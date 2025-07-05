// Blood Bank Management System - Main JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize all components
  initNavbar();
  initAnimations();
  initForms();
  initModals();
  initCounters();
  initScrollEffects();

  // Navbar functionality
  function initNavbar() {
    const navbar = document.getElementById("mainNavbar");
    if (navbar) {
      window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
          navbar.classList.add("scrolled");
        } else {
          navbar.classList.remove("scrolled");
        }
      });
    }

    // Mobile menu toggle
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector(".navbar-collapse");

    if (navbarToggler && navbarCollapse) {
      navbarToggler.addEventListener("click", function () {
        navbarCollapse.classList.toggle("show");
      });

      // Close mobile menu when clicking on links
      const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
      navLinks.forEach((link) => {
        link.addEventListener("click", function () {
          navbarCollapse.classList.remove("show");
        });
      });
    }
  }

  // Initialize animations
  function initAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in");
        }
      });
    }, observerOptions);

    // Observe elements with animation classes
    const animatedElements = document.querySelectorAll(
      ".feature-card, .stat-item, .about-content"
    );
    animatedElements.forEach((el) => {
      observer.observe(el);
    });
  }

  // Initialize form enhancements
  function initForms() {
    // Form validation and enhancement
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
      // Add custom styling to form inputs
      const inputs = form.querySelectorAll("input, select, textarea");
      inputs.forEach((input) => {
        input.classList.add("form-control-custom");

        // Add focus effects
        input.addEventListener("focus", function () {
          this.parentElement.classList.add("focused");
        });

        input.addEventListener("blur", function () {
          if (!this.value) {
            this.parentElement.classList.remove("focused");
          }
        });
      });

      // Form submission handling
      form.addEventListener("submit", function (e) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
          submitBtn.innerHTML = '<span class="loading"></span> Processing...';
          submitBtn.disabled = true;
        }
      });
    });

    // Newsletter form
    const newsletterForm = document.querySelector(".newsletter-form");
    if (newsletterForm) {
      newsletterForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        if (email) {
          showNotification("Thank you for subscribing!", "success");
          this.reset();
        }
      });
    }
  }

  // Initialize modal functionality
  function initModals() {
    // Custom modal triggers
    const modalTriggers = document.querySelectorAll("[data-modal]");
    modalTriggers.forEach((trigger) => {
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        const modalId = this.getAttribute("data-modal");
        const modal = document.getElementById(modalId);
        if (modal) {
          modal.classList.add("show");
          document.body.style.overflow = "hidden";
        }
      });
    });

    // Close modal functionality
    const modalCloses = document.querySelectorAll(
      ".modal-close, .modal-overlay"
    );
    modalCloses.forEach((close) => {
      close.addEventListener("click", function () {
        const modal = this.closest(".modal");
        if (modal) {
          modal.classList.remove("show");
          document.body.style.overflow = "";
        }
      });
    });
  }

  // Initialize counter animations
  function initCounters() {
    const counters = document.querySelectorAll(".stat-number");
    const observerOptions = {
      threshold: 0.5,
    };

    const counterObserver = new IntersectionObserver(function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const counter = entry.target;
          const target = parseInt(
            counter.getAttribute("data-target") ||
              counter.textContent.replace(/\D/g, "")
          );
          animateCounter(counter, target);
          counterObserver.unobserve(counter);
        }
      });
    }, observerOptions);

    counters.forEach((counter) => {
      counterObserver.observe(counter);
    });
  }

  // Animate counter numbers
  function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent =
        Math.floor(current) + (element.textContent.includes("+") ? "+" : "");
    }, 20);
  }

  // Initialize scroll effects
  function initScrollEffects() {
    // Parallax effect for hero section
    const heroSection = document.querySelector(".hero-section");
    if (heroSection) {
      window.addEventListener("scroll", function () {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        heroSection.style.transform = `translateY(${rate}px)`;
      });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach((link) => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });
  }

  // Notification system
  function showNotification(message, type = "info") {
    const notification = document.createElement("div");
    notification.className = `alert alert-${type} alert-custom alert-${type}-custom`;
    notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${getNotificationIcon(type)} mr-2"></i>
                <span>${message}</span>
                <button type="button" class="close ml-auto" onclick="this.parentElement.parentElement.remove()">
                    <span>&times;</span>
                </button>
            </div>
        `;

    // Add to page
    const container = document.querySelector(".container") || document.body;
    container.insertBefore(notification, container.firstChild);

    // Auto remove after 5 seconds
    setTimeout(() => {
      if (notification.parentElement) {
        notification.remove();
      }
    }, 5000);
  }

  function getNotificationIcon(type) {
    const icons = {
      success: "check-circle",
      warning: "exclamation-triangle",
      danger: "times-circle",
      info: "info-circle",
    };
    return icons[type] || "info-circle";
  }

  // Search functionality
  function initSearch() {
    const searchInput = document.querySelector(".search-input");
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        const items = document.querySelectorAll(".searchable-item");

        items.forEach((item) => {
          const text = item.textContent.toLowerCase();
          if (text.includes(query)) {
            item.style.display = "";
          } else {
            item.style.display = "none";
          }
        });
      });
    }
  }

  // Initialize search if present
  initSearch();

  // Utility functions
  window.BloodBankUtils = {
    showNotification: showNotification,
    animateCounter: animateCounter,
    formatDate: function (date) {
      return new Date(date).toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    },
    formatCurrency: function (amount) {
      return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
      }).format(amount);
    },
    debounce: function (func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },
  };

  // Add global error handling
  window.addEventListener("error", function (e) {
    console.error("Global error:", e.error);
    showNotification("An error occurred. Please try again.", "danger");
  });

  // Add offline/online detection
  window.addEventListener("online", function () {
    showNotification("You are back online!", "success");
  });

  window.addEventListener("offline", function () {
    showNotification(
      "You are currently offline. Some features may not work.",
      "warning"
    );
  });
});

// Additional utility functions
function copyToClipboard(text) {
  navigator.clipboard
    .writeText(text)
    .then(function () {
      BloodBankUtils.showNotification("Copied to clipboard!", "success");
    })
    .catch(function () {
      BloodBankUtils.showNotification("Failed to copy to clipboard", "danger");
    });
}

function downloadFile(url, filename) {
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Export functions for use in other scripts
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    copyToClipboard,
    downloadFile,
  };
}
