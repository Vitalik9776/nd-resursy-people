const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");
const overlay = document.querySelector(".nav-overlay");

const setMenu = (isOpen) => {
  header.classList.toggle("is-open", isOpen);
  toggle?.setAttribute("aria-expanded", String(isOpen));
  toggle?.setAttribute("aria-label", isOpen ? "Закрити меню" : "Відкрити меню");
  document.body.classList.toggle("no-scroll", isOpen);
};

toggle?.addEventListener("click", () => {
  setMenu(!header.classList.contains("is-open"));
});

overlay?.addEventListener("click", () => setMenu(false));

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setMenu(false);
});

document.querySelectorAll(".main-nav a, .header-actions a").forEach((link) => {
  link.addEventListener("click", () => setMenu(false));
});

const onScroll = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 10);
};

onScroll();
window.addEventListener("scroll", onScroll, { passive: true });
