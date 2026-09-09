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

// ── Global staggered scroll-reveal ──────────────────────────────────
// Called by: photos.js, project.js, blogs.js, and skills section in index.html
// container  – parent element to query inside
// selector   – CSS selector for items to animate (default '.scroll-reveal')
// stagger    – ms delay between each item (default 90)
window.initScrollAnim = function (container, selector, stagger) {
    selector = selector || '.scroll-reveal';
    stagger  = stagger  || 90;
    var items = container.querySelectorAll(selector);
    if (!items.length) return;

    var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var el = entry.target;
                setTimeout(function () {
                    el.classList.add('in-view');
                }, parseFloat(el.dataset.animDelay) || 0);
                obs.unobserve(el);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });

    items.forEach(function (el, i) {
        el.dataset.animDelay = i * stagger;
        obs.observe(el);
    });
};