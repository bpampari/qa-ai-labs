type SmartDOM = {
  inputs: any[];
  buttons: any[];
};

type Action =
  | { action: "fill"; selector: string; value: string }
  | { action: "click"; selector: string };

type Decision = {
  type: string;
  actions: Action[];
};

export function decideAction(dom: SmartDOM): Decision {

  const inputPlaceholders = dom.inputs.map(i => (i.placeholder || "").toLowerCase());
  const buttonTexts = dom.buttons.map(b => (b.text || "").toLowerCase());

  // Rule 1: Login Page Detection
  const isLoginPage =
    inputPlaceholders.some(p => p.includes("username") || p.includes("email")) &&
    inputPlaceholders.some(p => p.includes("password"));

  if (isLoginPage) {
    return {
      type: "login",
      actions: [
        { action: "fill", selector: "#userName", value: "testuser" },
        { action: "fill", selector: "#password", value: "password123" },
        { action: "click", selector: "#login" }
      ]
    };
  }

  // Rule 2: Generic Form
  if (dom.inputs.length > 0) {
    return {
      type: "form",
      actions: dom.inputs.map((input, index) => ({
        action: "fill",
        selector: `#${input.id}`,
        value: `test${index}`
      }))
    };
  }

  return {
    type: "unknown",
    actions: []
  };
}