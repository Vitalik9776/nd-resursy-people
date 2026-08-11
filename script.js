const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");
const overlay = document.querySelector(".nav-overlay");

const setMenu = (isOpen) => {
  header.classList.toggle("is-open", isOpen);
  toggle?.setAttribute("aria-expanded", String(isOpen));
  toggle?.setAttribute("aria-label", isOpen ? "Закрити меню" : "Відкрити меню");
  syncBodyScroll();
};

const syncBodyScroll = () => {
  const menuOpen = header?.classList.contains("is-open");
  const modalOpen = consultModal?.classList.contains("is-open");
  document.body.classList.toggle("no-scroll", Boolean(menuOpen || modalOpen));
};

toggle?.addEventListener("click", () => {
  setMenu(!header.classList.contains("is-open"));
});

overlay?.addEventListener("click", () => setMenu(false));

document.querySelectorAll(".main-nav a").forEach((link) => {
  link.addEventListener("click", () => setMenu(false));
});

const onScroll = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 10);
};

onScroll();
window.addEventListener("scroll", onScroll, { passive: true });

/* Consultation modal */

const TELEGRAM_FORM_URL = "https://konfiguratoronrender.onrender.com/telegram-form";
const consultModal = document.getElementById("consult-modal");
const consultForm = document.getElementById("consult-form");
const consultSubmit = document.getElementById("consult-submit");
const consultError = document.getElementById("consult-form-error");
const consultSuccess = document.getElementById("consult-form-success");
let lastFocus = null;
let closeTimer = null;

const ERROR_MESSAGES = {
  domain_not_found: "Не вдалося визначити домен сайту. Спробуйте ще раз.",
  site_not_registered: "Сайт ще не підключено до Telegram-бота.",
  internal_error: "Помилка сервера. Спробуйте пізніше.",
};

const setConsultState = ({ loading = false, error = "", success = false } = {}) => {
  if (consultSubmit) {
    consultSubmit.disabled = loading;
    consultSubmit.textContent = loading ? "Надсилання…" : "Надіслати";
  }

  if (consultError) {
    if (error) {
      consultError.hidden = false;
      consultError.textContent = error;
    } else {
      consultError.hidden = true;
      consultError.textContent = "";
    }
  }

  if (consultSuccess) {
    consultSuccess.hidden = !success;
  }
};

const openConsultModal = () => {
  if (!consultModal) return;
  clearTimeout(closeTimer);
  lastFocus = document.activeElement;
  setMenu(false);
  setConsultState();
  consultModal.hidden = false;
  requestAnimationFrame(() => {
    consultModal.classList.add("is-open");
  });
  syncBodyScroll();
  const firstField = consultForm?.querySelector("input, textarea, button");
  firstField?.focus();
};

const closeConsultModal = () => {
  if (!consultModal || (!consultModal.classList.contains("is-open") && consultModal.hidden)) {
    return;
  }
  clearTimeout(closeTimer);
  consultModal.classList.remove("is-open");
  syncBodyScroll();

  let closed = false;
  const finishClose = () => {
    if (closed) return;
    closed = true;
    consultModal.hidden = true;
    setConsultState();
    if (lastFocus && typeof lastFocus.focus === "function") {
      lastFocus.focus();
    }
  };

  consultModal.addEventListener("transitionend", finishClose, { once: true });
  closeTimer = setTimeout(finishClose, 280);
};

async function sendConsultationForm(data) {
  const response = await fetch(TELEGRAM_FORM_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: data.name,
      phone: data.phone,
      email: data.email || "",
      message: data.message || "",
      domain: window.location.hostname || undefined,
    }),
  });

  let result = {};
  try {
    result = await response.json();
  } catch {
    result = {};
  }

  if (!response.ok || !result.ok) {
    const code = result.error || result.message;
    const message =
      ERROR_MESSAGES[code] ||
      result.message ||
      "Не вдалося надіслати заявку. Спробуйте ще раз.";
    throw new Error(message);
  }

  return result;
}

document.querySelectorAll(".js-consult-open").forEach((trigger) => {
  trigger.addEventListener("click", () => openConsultModal());
});

consultModal?.querySelectorAll("[data-consult-close]").forEach((el) => {
  el.addEventListener("click", () => closeConsultModal());
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  if (consultModal?.classList.contains("is-open")) {
    closeConsultModal();
    return;
  }
  setMenu(false);
});

consultForm?.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(consultForm);
  const name = String(formData.get("name") || "").trim();
  const phone = String(formData.get("phone") || "").trim();
  const email = String(formData.get("email") || "").trim();
  const message = String(formData.get("message") || "").trim();

  if (!name || !phone) {
    setConsultState({ error: "Заповніть обов’язкові поля: ім’я та телефон." });
    return;
  }

  setConsultState({ loading: true });

  try {
    await sendConsultationForm({ name, phone, email, message });
    setConsultState({ loading: true, success: true });
    if (consultSubmit) consultSubmit.textContent = "Надіслано";
    consultForm.reset();
    closeTimer = setTimeout(() => closeConsultModal(), 1500);
  } catch (err) {
    setConsultState({
      error: err instanceof Error ? err.message : "Не вдалося надіслати заявку",
    });
  }
});
