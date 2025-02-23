function showSection(sectionId, buttonId) {
    const section = document.getElementById(sectionId);
    const button = document.getElementById(buttonId);
    let isVisible = false;
    button.addEventListener("click", function () {
        if (isVisible) {
            section.style.visibility = "hidden";
            section.style.display = "none";
            button.textContent = "Afficher";
        } else {
            section.style.visibility = "visible";
            section.style.display = "block";
            button.textContent = "Masquer";
        }
        isVisible = !isVisible;
    });
}