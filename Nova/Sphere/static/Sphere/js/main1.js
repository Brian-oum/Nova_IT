document.addEventListener("DOMContentLoaded", () => {
  // ======================
// PRELOADER
// ======================
const preloader = document.getElementById("preloader");

// Wait for all page resources (images, scripts, etc.) to load
window.addEventListener("load", () => {
  if (preloader) {
    // Keep preloader for 20 seconds, then fade out
    setTimeout(() => {
      preloader.classList.add("fade-out");
      setTimeout(() => {
        preloader.style.display = "none";
      }, 600); // Matches the fade transition in CSS
    }, 20000); // 20000ms = 20 seconds
  }
});

  // ======================
  // Menu Toggle & Dropdown on Mobile
  // ======================
  const menuToggle = document.getElementById('menu-toggle');
  const navbar = document.getElementById('navbar');
  const dropdownLinks = document.querySelectorAll('.dropdown > a');

  menuToggle?.addEventListener('click', () => {
    navbar?.classList.toggle('active');
    menuToggle.classList.toggle('active');

    // ✅ Always show header when menu is open
    document.body.classList.remove('header-hidden');
  });

  dropdownLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        link.parentElement.classList.toggle('active');
      }
    });
  });

  // ======================
  // Scroll Header Hide/Show (Fixed for Mobile)
  // ======================
  let lastScrollY = window.scrollY;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    const isMenuOpen = navbar?.classList.contains('active');

    // 🧩 Skip header hiding when the mobile menu is open
    if (!isMenuOpen) {
      if (currentScroll > lastScrollY && currentScroll > 100) {
        // Scrolling down → hide header
        document.body.classList.add('header-hidden');
      } else {
        // Scrolling up → show header
        document.body.classList.remove('header-hidden');
      }
    }

    lastScrollY = currentScroll;
  });

  // ======================
  // WhatsApp Get Quote Buttons
  // ======================
  const whatsappNumber = "254700780203";
  document.querySelectorAll(".get-quote").forEach(btn => {
    btn.addEventListener("click", e => {
      e.preventDefault();
      const product = btn.getAttribute("data-product");
      const message = `Hello! I'm interested in getting a quote for ${product}. Please share more details.`;
      const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
      window.open(url, "_blank");
    });
  });

  // ======================
  // Footer Year Update
  // ======================
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ======================
  // Animate on Scroll
  // ======================
  const animateElements = document.querySelectorAll('[data-animate]');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate');
        observer.unobserve(entry.target);
      }
    });
  });
  animateElements.forEach(el => observer.observe(el));

  // Reveal on scroll fallback
  const revealOnScroll = () => {
    animateElements.forEach(item => {
      const rect = item.getBoundingClientRect();
      if (rect.top < window.innerHeight - 100) {
        item.classList.add("visible");
      }
    });
  };
  window.addEventListener("scroll", revealOnScroll);
  revealOnScroll();

  // ======================
  // Slider
  // ======================
  const slides = document.querySelectorAll('.slider__slide');
  const dotsContainer = document.querySelector('.slider__dots');
  if (slides.length && dotsContainer) {
    let currentIndex = 0;

    // Create dots dynamically
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.addEventListener('click', () => showSlide(i));
      dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll('button');

    function showSlide(index) {
      slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
        dots[i].classList.toggle('active', i === index);
      });
      currentIndex = index;
    }

    function autoSlide() {
      currentIndex = (currentIndex + 1) % slides.length;
      showSlide(currentIndex);
    }

    setInterval(autoSlide, 8000); // Adjusted to 8 seconds for typical UX
    showSlide(0);
  }

  // ======================
  // Clients Slider
  // ======================
  const track = document.querySelector(".clients-track");
  const clientSlides = document.querySelectorAll(".client-slide");
  const clientDots = document.querySelectorAll(".clients-dots .dot");

  if (track && clientSlides.length && clientDots.length) {
    let currentIndex = 0;
    const totalSlides = clientSlides.length;

    function showClientSlide(index) {
      track.style.transform = `translateX(-${index * 100}%)`;
      clientDots.forEach(dot => dot.classList.remove("active"));
      clientDots[index].classList.add("active");
    }

    clientDots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        currentIndex = i;
        showClientSlide(currentIndex);
      });
    });

    setInterval(() => {
      currentIndex = (currentIndex + 1) % totalSlides;
      showClientSlide(currentIndex);
    }, 4000);

    showClientSlide(currentIndex);
  }

  // =======================
  // MODAL FUNCTIONALITY
  // =======================
  const modal = document.querySelector(".modal");
  if (modal) {
    const modalImage = modal.querySelector(".modal-content img");
    const modalTitle = modal.querySelector(".modal-content h3");
    const modalDescription = modal.querySelector(".modal-content p");
    const reviewsContainer = modal.querySelector(".reviews-section");
    const featuresContainer = modal.querySelector(".features-section");
    const modalClose = modal.querySelector(".modal-close");
    const readMoreButtons = document.querySelectorAll(".read-more");

    readMoreButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();

        // Retrieve data attributes
        const product = button.getAttribute("data-product");
        const imageSrc = button.getAttribute("data-image");
        const description = button.getAttribute("data-description");
        const reviewsData = button.getAttribute("data-reviews");
        const featuresData = button.getAttribute("data-features");

        // Fill modal content
        modalImage.src = imageSrc;
        modalTitle.textContent = product;
        modalDescription.textContent = description;

        // Features list
        featuresContainer.innerHTML = "";
        try {
          const features = JSON.parse(featuresData);
          if (features.length > 0) {
            const featuresHTML = features.map(f => `<li>${f}</li>`).join("");
            featuresContainer.innerHTML = `
              <h4>Key Features:</h4>
              <ul class="feature-list">${featuresHTML}</ul>
            `;
          }
        } catch (err) {
          console.error("Invalid features JSON:", err);
        }

        // Reviews list
        reviewsContainer.innerHTML = "";
        try {
          const reviews = JSON.parse(reviewsData);
          if (reviews.length > 0) {
            const reviewsHTML = reviews.map(r => `
              <div class="review-item">
                <p>"${r.review}"</p>
                <small>- ${r.name}</small>
              </div>
            `).join("");
            reviewsContainer.innerHTML = `
              <h4>Customer Reviews:</h4>
              ${reviewsHTML}
            `;
          }
        } catch (err) {
          console.error("Invalid reviews JSON:", err);
        }

        // Show modal
        modal.classList.add("show");
        document.body.classList.add("modal-open");
      });
    });

    // Close modal
    modalClose.addEventListener("click", () => {
      modal.classList.remove("show");
      document.body.classList.remove("modal-open");
    });

    // Close when clicking outside
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("show");
        document.body.classList.remove("modal-open");
      }
    });
  }
});
