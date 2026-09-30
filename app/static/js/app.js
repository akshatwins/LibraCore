document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[onsubmit]").forEach(form => {
    form.addEventListener("submit", event => {
      const message = form.getAttribute("onsubmit");
      if (message && message.includes("confirm(")) {
        // Native confirmation remains intentionally lightweight.
      }
    });
  });
});
