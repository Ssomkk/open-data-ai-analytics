/* ── Navbar scroll shadow ─────────────────────────────────────────── */
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
}

/* ── Mobile nav toggle ───────────────────────────────────────────── */
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', open);
  });
  // Close on link click
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

/* ── Stat cards — count-up animation ────────────────────────────── */
function animateCountUp(el) {
  const target = parseFloat(el.textContent.replace(/[^0-9.]/g, ''));
  if (isNaN(target) || target === 0) return;
  const duration = 900;
  const start = performance.now();
  const isFloat = el.textContent.includes('.');
  const step = ts => {
    const progress = Math.min((ts - start) / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    el.textContent = isFloat
      ? (target * ease).toFixed(2)
      : Math.round(target * ease);
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const valueEls = document.querySelectorAll('.stat-value');
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        animateCountUp(e.target);
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.5 });
  valueEls.forEach(el => observer.observe(el));
} else {
  valueEls.forEach(animateCountUp);
}

/* ── Visualizations — filter bar ────────────────────────────────── */
const filterBtns = document.querySelectorAll('.filter-btn');
const figureCards = document.querySelectorAll('.figure-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.filter;
    figureCards.forEach(card => {
      const name = card.dataset.name || '';
      const match = filter === 'all' || name.toLowerCase().includes(filter);
      card.classList.toggle('hidden', !match);
    });
  });
});

/* ── Lightbox ────────────────────────────────────────────────────── */
const lightbox   = document.getElementById('lightbox');
const lbImg      = document.getElementById('lightboxImg');
const lbCaption  = document.getElementById('lightboxCaption');
const lbClose    = document.getElementById('lightboxClose');

function openLightbox(src, caption) {
  if (!lightbox) return;
  lbImg.src = src;
  lbImg.alt = caption;
  lbCaption.textContent = caption;
  lightbox.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  lbClose.focus();
}

function closeLightbox() {
  if (!lightbox) return;
  lightbox.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  lbImg.src = '';
}

document.querySelectorAll('.btn-lightbox').forEach(btn => {
  btn.addEventListener('click', () => openLightbox(btn.dataset.src, btn.dataset.caption));
});

if (lbClose) lbClose.addEventListener('click', closeLightbox);
if (lightbox) {
  lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
}
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeLightbox();
});

/* ── Animate bar widths on scroll ────────────────────────────────── */
const bars = document.querySelectorAll('.station-bar, .yearly-bar');
if (bars.length && 'IntersectionObserver' in window) {
  const barObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.width = e.target.style.width; // trigger CSS transition
        barObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  bars.forEach(b => { const w = b.style.width; b.style.width = '0'; setTimeout(() => { b.style.width = w; }, 100); barObserver.observe(b); });
}

/* ── Fade-in on scroll (generic) ────────────────────────────────── */
const fadeEls = document.querySelectorAll('.card, .module-card, .figure-card, .figure-preview-card');
if ('IntersectionObserver' in window) {
  const fadeObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        fadeObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });
  fadeEls.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    fadeObs.observe(el);
  });
}
