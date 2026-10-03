const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const message = document.getElementById("message");
const togglePassword = document.getElementById("toggle-password");

togglePassword.addEventListener("click", () => {
  const hidden = passwordInput.type === "password";
  passwordInput.type = hidden ? "text" : "password";
  togglePassword.setAttribute("aria-label", hidden ? "Hide password" : "Show password");
});

function validationErrors(email, password) {
  const errors = [];
  if (!email.trim() || !password) {
    errors.push("Email and password are required.");
  }
  if (email.trim() && !email.includes("@")) {
    errors.push("Email must contain @.");
  }
  if (password && password.length < 8) {
    errors.push("Password must be at least 8 characters.");
  }
  return errors;
}

function showMessage(text, kind) {
  message.textContent = text;
  message.className = kind;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const email = emailInput.value;
  const password = passwordInput.value;
  const errors = validationErrors(email, password);
  if (errors.length) {
    showMessage(errors.join(" "), "error");
    return;
  }

  showMessage("Checking login.", "info");
  let response;
  try {
    response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
  } catch (err) {
    showMessage("Could not reach the server.", "error");
    return;
  }

  let data = {};
  try {
    data = await response.json();
  } catch (err) {
    showMessage("The server sent an unexpected response.", "error");
    return;
  }

  if (response.ok && data.ok) {
    showMessage("Signed in.", "ok");
    return;
  }
  showMessage(data.message || "Invalid email or password.", "error");
});
