// ================= MOBILE MENU =================
const mobileMenu = document.querySelector('.mobile-menu');
const navUl = document.querySelector('nav ul');

mobileMenu.addEventListener('click', () => {
  navUl.classList.toggle('active');
  mobileMenu.innerHTML = navUl.classList.contains('active')
    ? '<i class="fas fa-times"></i>'
    : '<i class="fas fa-bars"></i>';
});

// ================= DROPDOWN FUNCTIONALITY =================
const dropdowns = document.querySelectorAll('.dropdown');

function setupDropdowns() {
  dropdowns.forEach(dropdown => {
    const link = dropdown.querySelector('a:first-child');
    const newLink = link.cloneNode(true);
    link.parentNode.replaceChild(newLink, link);

    if (window.innerWidth > 768) {
      dropdown.addEventListener('mouseenter', () => dropdown.classList.add('active'));
      dropdown.addEventListener('mouseleave', () => dropdown.classList.remove('active'));
    } else {
      newLink.addEventListener('click', e => {
        e.preventDefault();
        dropdown.classList.toggle('active');
      });
    }
  });
}

setupDropdowns();
window.addEventListener('resize', setupDropdowns);

// ================= CLOSE DROPDOWNS WHEN CLICKING OUTSIDE =================
document.addEventListener('click', e => {
  if (!e.target.closest('.dropdown')) {
    dropdowns.forEach(dropdown => dropdown.classList.remove('active'));
  }
});

// ================= SMOOTH SCROLL =================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      window.scrollTo({
        top: target.offsetTop - 70,
        behavior: 'smooth'
      });
    }
    if (navUl.classList.contains('active')) {
      navUl.classList.remove('active');
      mobileMenu.innerHTML = '<i class="fas fa-bars"></i>';
    }
  });
});

// ================= INTERSECTION OBSERVER =================
const fadeElements = document.querySelectorAll('.fade-in');
const observer = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) entry.target.classList.add('animate');
    });
  },
  { threshold: 0.1 }
);
fadeElements.forEach(el => observer.observe(el));

// ================= TYPING ANIMATION =================
function initTypingAnimation() {
  const heading = document.querySelector('.services-text h2');
  if (!heading) return;
  const text = heading.textContent;
  const paragraph = document.querySelector('.services-text p');

  heading.innerHTML = '';
  if (paragraph) paragraph.style.opacity = '0';

  let i = 0;
  const typeHeading = setInterval(() => {
    if (i < text.length) {
      heading.innerHTML += text.charAt(i);
      i++;
    } else {
      clearInterval(typeHeading);
      if (paragraph) {
        setTimeout(() => {
          paragraph.style.transition = 'opacity 1.5s ease-in-out';
          paragraph.style.opacity = '1';
        }, 500);
      }
    }
  }, 100);
}

// ================= RESPONSIVE HANDLER =================
function handleResponsive() {
  const container = document.querySelector('.services-container');
  const grid = document.querySelector('.services-grid');
  if (!container || !grid) return;

  if (window.innerWidth <= 768) {
    container.style.flexDirection = 'column';
    grid.style.gridTemplateColumns = '1fr';
  } else {
    container.style.flexDirection = 'row';
    grid.style.gridTemplateColumns = 'repeat(2, 1fr)';
  }
}

// ================= RESPONSIVE BACKGROUND =================
function initResponsiveBackground() {
  const bgImage = document.querySelector('.section-bg img');
  if (!bgImage) return;

  function updateBackground() {
    const width = window.innerWidth;
    if (width < 768) {
      bgImage.style.filter = 'blur(1px) brightness(0.7)';
      bgImage.style.transform = 'scale(1.15)';
      bgImage.style.objectPosition = 'top center';
    } else if (width < 1024) {
      bgImage.style.filter = 'blur(2px) brightness(0.8)';
      bgImage.style.transform = 'scale(1.08)';
      bgImage.style.objectPosition = 'center center';
    } else {
      bgImage.style.filter = 'blur(3px) brightness(0.85)';
      bgImage.style.transform = 'scale(1.05)';
      bgImage.style.objectPosition = 'center center';
    }
  }

  bgImage.style.transition = 'all 5s ease';
  bgImage.style.objectFit = 'cover';
  bgImage.style.width = '100%';
  bgImage.style.height = '100%';

  updateBackground();
  window.addEventListener('resize', updateBackground);
}

// ================= SHAPE ANIMATOR =================
class ShapeAnimator {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.shapes = [];
    this.maxShapes = 15;
    if (this.container) this.init();
  }

  init() {
    this.createShapes();
    this.startAnimation();
  }

  createShapes() {
    const shapeTypes = ['circle', 'square', 'triangle', 'hexagon'];
    const colors = ['blue', 'purple', 'green', 'orange', 'pink'];

    for (let i = 0; i < this.maxShapes; i++) {
      const shape = document.createElement('div');
      const type = shapeTypes[Math.floor(Math.random() * shapeTypes.length)];
      const color = colors[Math.floor(Math.random() * colors.length)];

      shape.className = `shape ${type} ${color} glow`;
      const size = Math.random() * 60 + 20;
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const duration = Math.random() * 10 + 10;
      const delay = Math.random() * 5;

      shape.style.cssText = `
        width: ${size}px;
        height: ${type === 'triangle' ? 0 : size}px;
        left: ${left}%;
        top: ${top}%;
        animation-duration: ${duration}s;
        animation-delay: ${delay}s;
        opacity: ${Math.random() * 0.5 + 0.3};
      `;

      if (type === 'triangle') {
        shape.style.borderLeftWidth = `${size / 2}px`;
        shape.style.borderRightWidth = `${size / 2}px`;
        shape.style.borderBottomWidth = `${size}px`;
        shape.style.borderBottomColor = `rgba(255, 255, 255, 0.3)`;
      }

      this.container.appendChild(shape);
      this.shapes.push(shape);
    }
  }

  startAnimation() {
    this.shapes.forEach(shape => {
      const animations = ['float', 'pulse', 'spin'];
      const randomAnimation = animations[Math.floor(Math.random() * animations.length)];
      if (randomAnimation === 'spin') {
        shape.style.animation = `spin ${Math.random() * 20 + 10}s linear infinite`;
      } else if (randomAnimation === 'pulse') {
        shape.style.animation = `pulse ${Math.random() * 3 + 2}s ease-in-out infinite`;
      }
    });
  }
}

// ================= HERO SLIDESHOW (FADE VERSION) =================
document.addEventListener('DOMContentLoaded', function() {
  const slides = document.querySelectorAll('.slide');
  const dots = document.querySelectorAll('.dot');
  let currentSlide = 0;
  const totalSlides = slides.length;

  function showSlide(index) {
    slides.forEach((s, i) => s.classList.toggle('active', i === index));
    dots.forEach((d, i) => d.classList.toggle('active', i === index));
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
  }

  let slideInterval = setInterval(nextSlide, 6000);

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      clearInterval(slideInterval);
      showSlide(index);
      currentSlide = index;
      slideInterval = setInterval(nextSlide, 6000);
    });
  });

  // Show first slide immediately
  showSlide(0);
});

// ================= ALERT AUTO-DISMISS =================
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(alert => {
    alert.style.transition = 'opacity 0.5s ease';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 800);
  });
}, 4000);

// ================= INITIALIZATION =================
window.addEventListener('load', () => {
  initTypingAnimation();
  handleResponsive();
  initResponsiveBackground();

  const shapeAnimator = new ShapeAnimator('animatedShapes');

  const modernServicesSection = document.querySelector('.modern-services');
  if (modernServicesSection) {
    modernServicesSection.addEventListener('mouseenter', () => {
      shapeAnimator.shapes.forEach(shape => (shape.style.animationDuration = '3s'));
    });
    modernServicesSection.addEventListener('mouseleave', () => {
      shapeAnimator.shapes.forEach(shape => {
        const duration = Math.random() * 10 + 10;
        shape.style.animationDuration = `${duration}s`;
      });
    });
  }
});

window.addEventListener('resize', handleResponsive);
