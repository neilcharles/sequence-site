// Small-screen menu: fold behind the button. Without script it stays open.
(function () {
  var button = document.querySelector(".nav-toggle");
  if (!button) return;
  button.hidden = false;
  button.addEventListener("click", function () {
    var open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
  });
})();
