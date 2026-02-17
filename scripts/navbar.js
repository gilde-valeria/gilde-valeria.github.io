export function initNavbar() {
  const toggleBtn = document.querySelector('.nav-toggle');
  const menu = document.querySelector('.nav-menu');
  const navbar = document.querySelector('.navbar');

  if (!toggleBtn || !menu || !navbar) return;

  function closeMenu() {
    menu.classList.remove('show');
    document.body.classList.remove('menu-open');
  }

  toggleBtn.addEventListener('click', () => {
    menu.classList.toggle('show');
    document.body.classList.toggle('menu-open');
  });

  document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) closeMenu();
  });

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) navbar.classList.add('scrolled');
    else navbar.classList.remove('scrolled');
  });
}