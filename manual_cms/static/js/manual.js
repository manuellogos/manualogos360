// Manual JavaScript - Funcionalidades interactivas

// Función para cambiar idioma
function switchLanguage(langCode) {
  const currentPath = window.location.pathname;
  let newPath;

  // Detectar el idioma actual de la URL
  const currentLangMatch = currentPath.match(/^\/([a-z]{2})\//);
  const currentLang = currentLangMatch ? currentLangMatch[1] : "es";

  if (langCode === "es") {
    // Ir a español (sin prefijo)
    if (currentLangMatch) {
      newPath = currentPath.replace(/^\/[a-z]{2}/, "");
      if (newPath === "") newPath = "/";
    } else {
      newPath = currentPath; // Ya estamos en español
    }
  } else {
    // Ir a otro idioma
    if (currentLangMatch) {
      // Reemplazar el prefijo existente
      newPath = currentPath.replace(/^\/[a-z]{2}/, "/" + langCode);
    } else {
      // Añadir prefijo al español
      newPath = "/" + langCode + currentPath;
    }
  }

  // Intentar la nueva URL
  window.location.href = newPath;
}

document.addEventListener("DOMContentLoaded", function () {
  // Toggle del sidebar en mobile
  const sidebarToggle = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });

    // Cerrar sidebar al hacer clic fuera en mobile
    document.addEventListener("click", function (e) {
      if (window.innerWidth <= 767) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
          sidebar.classList.remove("active");
        }
      }
    });
  }

  // Smooth scrolling para anclas
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Highlighting del código con Prism.js
  if (typeof Prism !== "undefined") {
    Prism.highlightAll();
  }

  // Mejorar la navegación del sidebar
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".sidebar .nav-link");

  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");

      // Expandir secciones padre si es necesario
      let parent = link.closest(".nav-subsection");
      if (parent) {
        parent.classList.add("expanded");
      }
    }
  });

  // Funcionalidad de búsqueda en la sidebar (opcional)
  const searchInput = document.getElementById("sidebarSearch");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const navItems = document.querySelectorAll(".sidebar .nav-link");

      navItems.forEach((item) => {
        const text = item.textContent.toLowerCase();
        const parent = item.closest(
          ".nav-section, .nav-subsection, .nav-article"
        );

        if (text.includes(searchTerm) || searchTerm === "") {
          parent.style.display = "";
        } else {
          parent.style.display = "none";
        }
      });
    });
  }

  // Copiado de código al hacer clic
  document.querySelectorAll(".code-block pre").forEach((codeBlock) => {
    // Crear botón de copia
    const copyButton = document.createElement("button");
    copyButton.className = "btn btn-sm btn-outline-secondary copy-code-btn";
    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
    copyButton.title = "Copiar código";

    // Posicionar el botón
    codeBlock.style.position = "relative";
    copyButton.style.position = "absolute";
    copyButton.style.top = "10px";
    copyButton.style.right = "10px";
    copyButton.style.zIndex = "10";

    codeBlock.appendChild(copyButton);

    // Funcionalidad de copia
    copyButton.addEventListener("click", function () {
      const code = codeBlock.querySelector("code");
      const text = code.textContent;

      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          copyButton.innerHTML = '<i class="fas fa-check"></i>';
          copyButton.classList.replace("btn-outline-secondary", "btn-success");

          setTimeout(() => {
            copyButton.innerHTML = '<i class="fas fa-copy"></i>';
            copyButton.classList.replace(
              "btn-success",
              "btn-outline-secondary"
            );
          }, 2000);
        });
      } else {
        // Fallback para navegadores más antiguos
        const textArea = document.createElement("textarea");
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand("copy");
        document.body.removeChild(textArea);

        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        copyButton.classList.replace("btn-outline-secondary", "btn-success");

        setTimeout(() => {
          copyButton.innerHTML = '<i class="fas fa-copy"></i>';
          copyButton.classList.replace("btn-success", "btn-outline-secondary");
        }, 2000);
      }
    });
  });

  // Tabla de contenidos automática para artículos largos
  const article = document.querySelector(".manual-article");
  if (article) {
    const headings = article.querySelectorAll("h2, h3, h4");

    if (headings.length > 3) {
      const toc = createTableOfContents(headings);
      const articleHeader = article.querySelector(".article-header");
      if (articleHeader && toc) {
        articleHeader.appendChild(toc);
      }
    }
  }

  // Funciones auxiliares
  function createTableOfContents(headings) {
    if (headings.length === 0) return null;

    const tocContainer = document.createElement("div");
    tocContainer.className = "table-of-contents";
    tocContainer.innerHTML = '<h5><i class="fas fa-list"></i> Contenido</h5>';

    const tocList = document.createElement("ul");
    tocList.className = "toc-list";

    headings.forEach((heading, index) => {
      // Asignar ID si no lo tiene
      if (!heading.id) {
        heading.id = `heading-${index}`;
      }

      const listItem = document.createElement("li");
      listItem.className = `toc-item toc-${heading.tagName.toLowerCase()}`;

      const link = document.createElement("a");
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent;
      link.className = "toc-link";

      listItem.appendChild(link);
      tocList.appendChild(listItem);
    });

    tocContainer.appendChild(tocList);
    return tocContainer;
  }

  // Lazy loading para imágenes
  const images = document.querySelectorAll("img[data-src]");
  if (images.length > 0) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute("data-src");
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach((img) => imageObserver.observe(img));
  }

  // Mejorar la accesibilidad del teclado
  document.addEventListener("keydown", function (e) {
    // Escapar para cerrar sidebar en mobile
    if (e.key === "Escape" && sidebar && sidebar.classList.contains("active")) {
      sidebar.classList.remove("active");
    }

    // Navegación con teclas de flecha en la sidebar
    if (e.target.classList.contains("nav-link")) {
      const navLinks = Array.from(
        document.querySelectorAll(".sidebar .nav-link")
      );
      const currentIndex = navLinks.indexOf(e.target);

      if (e.key === "ArrowDown") {
        e.preventDefault();
        const nextIndex = (currentIndex + 1) % navLinks.length;
        navLinks[nextIndex].focus();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        const prevIndex =
          currentIndex > 0 ? currentIndex - 1 : navLinks.length - 1;
        navLinks[prevIndex].focus();
      }
    }
  });

  // Inicializar tooltips de Bootstrap si están disponibles
  if (typeof bootstrap !== "undefined" && bootstrap.Tooltip) {
    const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }

  // Efecto de lectura progresiva
  const progressBar = createReadingProgressBar();
  if (progressBar && article) {
    document.body.appendChild(progressBar);
    updateReadingProgress();

    window.addEventListener("scroll", updateReadingProgress);
    window.addEventListener("resize", updateReadingProgress);
  }

  function createReadingProgressBar() {
    const progressContainer = document.createElement("div");
    progressContainer.className = "reading-progress";
    progressContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: rgba(0, 123, 255, 0.1);
            z-index: 1051;
        `;

    const progressBar = document.createElement("div");
    progressBar.className = "progress-bar";
    progressBar.style.cssText = `
            height: 100%;
            background-color: var(--primary-color);
            transition: width 0.1s ease;
            width: 0%;
        `;

    progressContainer.appendChild(progressBar);
    return progressContainer;
  }

  function updateReadingProgress() {
    const article = document.querySelector(".manual-article");
    if (!article) return;

    const articleTop = article.offsetTop;
    const articleHeight = article.offsetHeight;
    const windowHeight = window.innerHeight;
    const scrollTop = window.pageYOffset;

    const progress = Math.min(
      Math.max((scrollTop - articleTop + windowHeight) / articleHeight, 0),
      1
    );

    const progressBar = document.querySelector(
      ".reading-progress .progress-bar"
    );
    if (progressBar) {
      progressBar.style.width = `${progress * 100}%`;
    }
  }

  // Modal de galería de imágenes
  const imageModal = document.getElementById("imageModal");
  if (imageModal) {
    const modalImage = document.getElementById("modalImage");
    const modalTitle = document.getElementById("imageModalLabel");

    imageModal.addEventListener("show.bs.modal", function (event) {
      const button = event.relatedTarget;
      const imageSrc = button.getAttribute("data-bs-image");
      const imageTitle = button.getAttribute("data-bs-title");

      modalImage.src = imageSrc;
      modalTitle.textContent = imageTitle || "Imagen";
    });
  }

  console.log("Manual JavaScript initialized successfully");
});
