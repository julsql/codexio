const firstPage = document.getElementById("first-page");
const prevPage = document.getElementById("prev-page");
const currentPage = document.getElementById("current-page");
const nextPage = document.getElementById("next-page");
const lastPage = document.getElementById("last-page");

firstPage.addEventListener("selectstart", function (e) {e.preventDefault();});
prevPage.addEventListener("selectstart", function (e) {e.preventDefault();});
currentPage.addEventListener("selectstart", function (e) {e.preventDefault();});
nextPage.addEventListener("selectstart", function (e) {e.preventDefault();});
lastPage.addEventListener("selectstart", function (e) {e.preventDefault();});

const paginationItems = document.querySelectorAll(".pagination-item");
const itemsPerPage = 20;
const nbPage = Math.ceil(paginationItems.length / itemsPerPage);
let currentPageInt = 1;

function displayPage(pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    paginationItems.forEach((item, index) => {
        if (index >= startIndex && index < endIndex) {
            item.style.visibility = "visible";
            item.style.display = "block";
        } else {
            item.style.visibility = "hidden";
            item.style.display = "none";
        }
    });
    currentPage.textContent = pageNumber + "/" + nbPage
    if (currentPageInt === 1) {
        firstPage.style.visibility = "hidden"
        prevPage.style.visibility = "hidden"
    }
    else {
        firstPage.style.visibility = "visible"
        prevPage.style.visibility = "visible"
    }
    if (currentPageInt === nbPage) {
        lastPage.style.visibility = "hidden"
        nextPage.style.visibility = "hidden"
    }
    else {
        lastPage.style.visibility = "visible"
        nextPage.style.visibility = "visible"
    }

}
document.getElementById("prev-page").addEventListener("click", function () {
    if (currentPageInt > 1) {
        currentPageInt--;
        displayPage(currentPageInt);
    }
});

document.getElementById("next-page").addEventListener("click", function () {

    if (currentPageInt < nbPage) {
        currentPageInt++;
        displayPage(currentPageInt);
    }
});

document.getElementById("first-page").addEventListener("click", function () {

    if (currentPageInt > 1) {
        currentPageInt = 1;
        displayPage(currentPageInt);
    }
});

lastPage.addEventListener("click", function () {

    if (currentPageInt < nbPage) {
        currentPageInt = nbPage;
        displayPage(currentPageInt);
    }
});

displayPage(currentPageInt);