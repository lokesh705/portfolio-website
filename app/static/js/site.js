const form = document.getElementById("contact-form");
const status = document.getElementById("contact-status");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(form).entries());
    status.textContent = "Sending...";
    status.className = "status";
    const response = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (response.ok) {
      form.reset();
      status.textContent = "Thanks! Your message has been sent.";
      status.className = "status ok";
    } else {
      status.textContent = data.error || "Something went wrong.";
      status.className = "status err";
    }
  });
}
