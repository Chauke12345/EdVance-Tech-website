document.addEventListener("DOMContentLoaded", function () {
  // Mobile navigation: support both original and redesigned class names.
  const menuToggle = document.querySelector(".menu-toggle");
  const mainNav = document.querySelector(".main-nav");
  if (menuToggle && mainNav) {
    menuToggle.addEventListener("click", function () {
      const isOpen = mainNav.classList.contains("is-open") || mainNav.classList.contains("active");
      mainNav.classList.toggle("is-open", !isOpen);
      mainNav.classList.toggle("active", !isOpen);
      menuToggle.setAttribute("aria-expanded", String(!isOpen));
      menuToggle.setAttribute("aria-label", isOpen ? "Open navigation menu" : "Close navigation menu");
      menuToggle.textContent = isOpen ? "☰" : "✕";
    });
    mainNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mainNav.classList.remove("is-open", "active");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.setAttribute("aria-label", "Open navigation menu");
        menuToggle.textContent = "☰";
      });
    });
  }

  // Package links: prefill the service selector on the contact page.
  document.querySelectorAll("[data-package]").forEach(function (link) {
    link.addEventListener("click", function () {
      const selectedPackage = link.getAttribute("data-package");
      const field = document.querySelector("#service, #serviceSelect");
      if (field && selectedPackage) field.value = selectedPackage;
    });
  });

  // Support service/project/package links that pass values in the URL.
  const params = new URLSearchParams(window.location.search);
  const serviceField = document.querySelector("#service, #serviceSelect");
  if (serviceField) {
    const service = params.get("service") || params.get("package");
    if (service) {
      const option = Array.from(serviceField.options || []).find(o => o.value === service || o.textContent.trim() === service);
      if (option) serviceField.value = option.value || option.textContent.trim();
    }
  }
  const messageField = document.querySelector("#message, textarea[name='message']");
  const project = params.get("project");
  if (messageField && project && !messageField.value) messageField.value = "I'm interested in discussing the " + project.replace(/-/g, " ") + " project.";
  if (messageField && params.get("subject") && !messageField.value) messageField.value = "Business partnership enquiry";

  // Keep the original form's WhatsApp submission behaviour.
  const quoteForm = document.getElementById("quoteForm");
  if (quoteForm) {
    quoteForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const name = quoteForm.elements["name"]?.value || "";
      const email = quoteForm.elements["email"]?.value || "";
      const phone = quoteForm.elements["phone"]?.value || "Not provided";
      const service = quoteForm.elements["service"]?.value || "General enquiry";
      const message = quoteForm.elements["message"]?.value || "";
      const whatsappMessage = `Hello EdVance Tech,

I would like to request a quote.

Name: ${name}
Email: ${email}
Phone: ${phone}
Service: ${service}

Project Details:
${message}`;
      window.location.href = "https://wa.me/27733141222?text=" + encodeURIComponent(whatsappMessage);
    });
  }
});
