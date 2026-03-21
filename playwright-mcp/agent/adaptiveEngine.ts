type ValidationResult = {
  success: boolean;
  message: string;
};

type Action =
  | { action: "fill"; selector: string; value: string }
  | { action: "click"; selector: string };

export function adaptStrategy(result: ValidationResult,previousActions: Action[]): Action[]  {

  console.log("🧠 Adapting based on result:", result.message);

  // 🔹 Case 1: Invalid credentials
  if (result.message.toLowerCase().includes("invalid")) {

    return [
      { action: "fill", selector: "#userName", value: "testuser2" },
      { action: "fill", selector: "#password", value: "password123" },
      { action: "click", selector: "#login" }
    ];
  }

  // 🔹 Case 2: Unknown failure
  return [
    { action: "fill", selector: "#userName", value: "admin" },
    { action: "fill", selector: "#password", value: "admin123" },
    { action: "click", selector: "#login" }
  ];
}