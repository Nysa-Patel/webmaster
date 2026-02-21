const hero = document.querySelector('.hero');

window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  const scale = Math.max(0.92, 1 - scrolled * 0.0001);
  hero.style.transform = `scale(${scale})`;
});