import { openPage, getSmartDOM, fill, click } from '../mcp/server.js';
import { decideAction } from './decisionEngine.js';
import { validateLogin } from './validator.js';
import { adaptStrategy } from './adaptiveEngine.js';
import * as actions from '../mcp/server.js';
import { getLLMActions } from './llmEngine.js';


async function executeActions(actionList: any[]) {

  for (const act of actionList) {

    if (act.action === "fill") {
      console.log(`Filling ${act.selector} with ${act.value}`);
      await fill(act.selector, act.value);
    }

    if (act.action === "click") {
      console.log(`Clicking ${act.selector}`);
      await click(act.selector);
    }

  }
}

async function runAgent() {
  console.log("Available actions:", Object.keys(actions));
  console.log("Step 1: Opening page...");
  await openPage("https://demoqa.com/login");

  console.log("Step 2: Extracting DOM...");
  const dom = await getSmartDOM();

  console.log("Step 3: Initial decision...");
  let decision = decideAction(dom);

  let attempts = 0;
  const maxAttempts = 3;
  let lastResult = {
      success: false,
      message: "initial run"
      };
 while (attempts < maxAttempts) {

   console.log(`\n🚀 Attempt ${attempts + 1}`);

   // 🧠 Step 1: Ask LLM what to do
   const actionsFromLLM = await getLLMActions({
     dom,
     lastResult
   });

   console.log("🤖 LLM Suggested Actions:", actionsFromLLM);

   // ⚠️ Safety check
   if (!actionsFromLLM || actionsFromLLM.length === 0) {
     console.log("❌ No valid actions from LLM");
     attempts++;
     continue;
   }

   // 🧪 Step 2: Execute actions
   await executeActions(actionsFromLLM);

   // 🔍 Step 3: Validate
   console.log("Step: Validating...");
   const result = await validateLogin(actions);

   console.log("Validation:", result);

   // ✅ Step 4: Success check
   if (result.success) {
     console.log("✅ Test Passed");
     return;
   }

   // 🔁 Step 5: Update context for next attempt
   lastResult = result;

   attempts++;
 }

  console.log("❌ All attempts failed");

}

runAgent();