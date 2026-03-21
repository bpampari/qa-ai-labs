type ValidationResult = {
  success: boolean;
  message: string;
};

export async function validateLogin(actions: any): Promise<ValidationResult> {

  try {

    console.log("⏳ Waiting for UI update...");

    // 🔥 Wait a bit for navigation/update
    await new Promise(res => setTimeout(res, 3000));

    console.log("🔍 Checking for success indicators...");

    // ✅ Check logout button text (strong signal)
    const buttonText = await actions.getText("#submit");

    if (buttonText && buttonText.toLowerCase().includes("log out")) {
      return {
        success: true,
        message: "Login successful (Logout button detected)"
      };
    }

    // ✅ Check username display (another strong signal)
    const usernameVisible = await actions.waitForSelector("#userName-value", 2000);

    if (usernameVisible) {
      return {
        success: true,
        message: "Login successful (User profile visible)"
      };
    }

    console.log("🔍 Checking for error indicators...");

    // ❌ Check error message
    const errorText = await actions.getText("#name");

    if (errorText && errorText.toLowerCase().includes("invalid")) {
      return {
        success: false,
        message: errorText
      };
    }

    return {
      success: false,
      message: "No clear success or failure signal"
    };

  } catch (e) {
    console.log("Validator exception:", e);

    return {
      success: false,
      message: "Validation exception occurred"
    };
  }
}