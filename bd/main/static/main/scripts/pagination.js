function paginate(classFirstPage, classPrevPage, classCurrentPage, classNextPage, classLastPage, classPaginationItem, idDiv) {
    const firstPage = document.getElementById(classFirstPage);
    const prevPage = document.getElementById(classPrevPage);
    const currentPage = document.getElementById(classCurrentPage);
    const nextPage = document.getElementById(classNextPage);
    const lastPage = document.getElementById(classLastPage);
    const container = document.getElementById(idDiv);

    firstPage.addEventListener("selectstart", function (e) {e.preventDefault();});
    prevPage.addEventListener("selectstart", function (e) {e.preventDefault();});
    currentPage.addEventListener("selectstart", function (e) {e.preventDefault();});
    nextPage.addEventListener("selectstart", function (e) {e.preventDefault();});
    lastPage.addEventListener("selectstart", function (e) {e.preventDefault();});

    const paginationItems = document.querySelectorAll(classPaginationItem);
    const itemsPerPage = 10;
    const nbPage = Math.ceil(paginationItems.length / itemsPerPage);
    let currentPageInt = 1;

    function displayPage(pageNumber) {
        if (paginationItems.length === 0) {
            container.style.visibility = "hidden";
            container.style.display = "none";
            return;
        }
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

    prevPage.addEventListener("click", function () {
        if (currentPageInt > 1) {
            currentPageInt--;
            displayPage(currentPageInt);
        }
    });

    nextPage.addEventListener("click", function () {

        if (currentPageInt < nbPage) {
            currentPageInt++;
            displayPage(currentPageInt);
        }
    });

    firstPage.addEventListener("click", function () {

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
}