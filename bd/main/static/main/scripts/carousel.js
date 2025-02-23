function useCarousel(classCarousel, idNext, idPrev, classImages) {

    const carousel = document.querySelector(classCarousel);
    const next = document.querySelector(idNext);
    const prev = document.querySelector(idPrev);
    const images = document.querySelectorAll(classImages);

    function hideItem(item) {
        item.style.visibility = "hidden";
        item.style.display = "none";
    }
    function showItem(item) {
        item.style.visibility = "visible";
        item.style.display = "flex";
    }

    if (images.length > 1) {
        showItem(next);
        showItem(prev);
    } else {
        hideItem(next);
        hideItem(prev);
    }

    let currentIndexImage = 0; // Index de l'image affichée

    // Fonction pour centrer l'image actuelle
    function centerImage(index) {
        if (images.length === 0) return;
        const image = images[index];
        const carouselWidth = carousel.clientWidth;
        const imageWidth = image.clientWidth;
        const imageOffsetLeft = image.offsetLeft;

        // Calcul pour centrer l'image
        const scrollPosition = imageOffsetLeft - (carouselWidth / 2) + (imageWidth / 2);
        carousel.scrollTo({ left: scrollPosition, behavior: "smooth" });
    }

    // Fonction pour aller à l'image suivante
    function nextImage() {
        if (currentIndexImage < images.length - 1) {
            currentIndexImage++;
        } else {
            currentIndexImage = 0;
        }
        centerImage(currentIndexImage);
        console.log(currentIndexImage)
    }

    function prevImage() {
        if (currentIndexImage > 0) {
            currentIndexImage--;
        } else {
            currentIndexImage = images.length - 1;
        }
        centerImage(currentIndexImage);
        console.log(currentIndexImage)
    }

    // Ajout des événements sur les boutons
    next.addEventListener("click", nextImage);
    prev.addEventListener("click", prevImage);

    function getOffsetLeftFromParent(element, parent) {
        const elementRect = element.getBoundingClientRect();
        const parentRect = parent.getBoundingClientRect();
        return elementRect.left - parentRect.left;
    }

    carousel.addEventListener("scroll", () => {
        let closestIndex = 0;
        let minDifference = Infinity;

        images.forEach((img, index) => {
            const diff = carousel.offsetWidth/2 - (getOffsetLeftFromParent(img, carousel) + img.width/2);
            if (Math.abs(diff) < minDifference) {
                closestIndex = index;
                minDifference = diff;
            }
        });
        if (Math.abs(minDifference) > 5) {
            if (closestIndex === 1) {
                closestIndex = 0;
            } else if (closestIndex === images.length - 2) {
                closestIndex = images.length -1
            }
        }
        currentIndexImage = closestIndex;
    });
}
