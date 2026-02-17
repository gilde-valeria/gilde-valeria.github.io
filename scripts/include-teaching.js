import { initNavbar } from './navbar.js';

async function loadInto(selector, url) {
  const el = document.querySelector(selector);
  if (!el) return;
  const res = await fetch(url);
  if (!res.ok) return;
  el.innerHTML = await res.text();
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadInto('#site-navbar', '/components/navbar-teaching.html');
  await loadInto('#site-footer', '/components/footer.html');
  // await loadInto('#site-footer', '/components/footer-teaching.html'); // opcional
  initNavbar();
});