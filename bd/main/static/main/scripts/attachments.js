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
    window.scrollTo({ top: 0, behavior: "smooth" });
}
