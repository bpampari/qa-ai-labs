import axios from "axios";

type LLMContext = {
  dom: any;
  lastResult: any;
};

export async function getLLMActions(context: LLMContext) {

  const prompt = `
You are a QA automation agent.

Page elements:
${JSON.stringify(context.dom, null, 2)}

Last result:
${JSON.stringify(context.lastResult, null, 2)}

Return ONLY JSON:
[
  { "action": "fill", "selector": "#userName", "value": "testuser" },
  { "action": "fill", "selector": "#password", "value": "Test@123" },
  { "action": "click", "selector": "#login" }
]
`;

  const response = await axios.post("http://localhost:11434/api/generate", {
    model: "llama3",
    prompt: prompt,
    stream: false
  });

  function extractJSON(text: string) {
    const match = text.match(/\[.*\]/s);
    if (!match) return null;

    try {
      return JSON.parse(match[0]);
    } catch {
      return null;
    }
  }

const raw = response.data.response;
const parsed = extractJSON(raw);

if (!parsed) {
  console.log("⚠️ Failed to parse LLM response");
  return [];
}

return parsed;
}