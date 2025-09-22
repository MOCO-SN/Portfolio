document.onkeydown = (e) => {
    if (e.key == 123) {
        e.preventDefault();
    }
    if (e.ctrlKey && e.shiftKey && e.key == 'I') {
        e.preventDefault();
    }
    if (e.ctrlKey && e.shiftKey && e.key == 'C') {
        e.preventDefault();
    }
    if (e.ctrlKey && e.shiftKey && e.key == 'J') {
        e.preventDefault();
    }
    if (e.ctrlKey && e.key == 'U') {
        e.preventDefault();
    }
};



const scrollLine = document.querySelector('.scroll-line');

function updateScrollProgress() {
  const windowHeight = window.innerHeight;
  const fullHeight = document.body.clientHeight;
  const scrolled = window.scrollY;
  const percentScrolled = (scrolled / (fullHeight - windowHeight)) * 100;
  scrollLine.style.width = `${percentScrolled}%`;
}

updateScrollProgress();

let ticking = false;
window.addEventListener('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      updateScrollProgress();
      ticking = false;
    });
    ticking = true;
  }
});

window.addEventListener('resize', updateScrollProgress);