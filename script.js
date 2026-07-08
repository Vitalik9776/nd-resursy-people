const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");

toggle?.addEventListener("click", () => {
  const isOpen = header.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(isOpen));
});

document.querySelectorAll(".main-nav a").forEach((link) => {
  link.addEventListener("click", () => {
    header.classList.remove("is-open");
    toggle?.setAttribute("aria-expanded", "false");
  });
});
