function showSection(sectionId, buttonId) {
    const section = document.getElementById(sectionId);
    const button = document.getElementById(buttonId);
    let isVisible = false;
    button.addEventListener("click", function () {
        if (isVisible) {
            section.style.display = "none";
            button.textContent = "Afficher";
        } else {
            section.style.display = "block";
            button.textContent = "Masquer";
        }
        isVisible = !isVisible;
    });
}

// Affiche le bouton si on scroll vers le bas
window.onscroll = function () {
    let scrollTopBtn = document.getElementById("scrollTopBtn");
    if (document.documentElement.scrollTop > 300) {
        scrollTopBtn.style.display = "flex";
    } else {
        scrollTopBtn.style.display = "none";
    }
};

// Fonction pour remonter en haut
function scrollToTop() {
    window.scrollTo({top: 0, behavior: "smooth"});
}

document.addEventListener('DOMContentLoaded', function () {
    // Fonction pour charger l'image lorsqu'elle devient visible
    function loadImage(entry) {
        const image = entry.target;
        const src = image.getAttribute('data-src');
        if (src) {
            image.setAttribute('src', src);  // Charger l'image
            image.removeAttribute('data-src');  // Supprimer l'attribut data-src
        }
    }

    // Observer les images uniquement lorsque celles-ci deviennent visibles
    const observerOptions = {
        root: null, // observer par rapport au viewport
        rootMargin: '0px',
        threshold: 0.1  // L'image doit être à 10% visible pour être chargée
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadImage(entry);
                observer.unobserve(entry.target);  // Arrêter d'observer une fois l'image chargée
            }
        });
    }, observerOptions);

    // Observer toutes les images
    document.querySelectorAll('img[data-src]').forEach(image => {
        observer.observe(image);
    });

    // Implémentation du scroll infini (si vous chargez plus de contenus au défilement)
    window.addEventListener('scroll', function () {
        const bottomOfPage = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight;
        if (bottomOfPage) {
            // Ajouter du contenu dynamique (ici on peut appeler une fonction AJAX ou charger plus de contenu)
            console.log('Chargement des nouveaux éléments...');
        }
    });
});
