const seeMoreButton = document.getElementById("see-more");
const arrow = document.querySelector(".arrow");
const upperLine = document.getElementById("upper-line");
const lowerLine = document.getElementById("lower-line");

let seeMore = false;

seeMoreButton.addEventListener("click", (event) => {
    document.querySelectorAll('[data-see="false"]').forEach(function(element) {
        console.log(window.innerWidth);
        if (window.innerWidth < 800) {
            element.style.display = seeMore ? "none" : "block";
        } else {
            element.style.display = seeMore ? "none" : "table-cell";
        }
    });
    seeMore = !seeMore;

    if (window.innerWidth < 800) {
        upperLine.style.display = "none";
        lowerLine.style.display = "none";
    } else {
        upperLine.style.display = seeMore ? "none" : "block";
        lowerLine.style.display = seeMore ? "block" : "none";
    }
    arrow.style.transform = seeMore ? "rotate(0deg)" : "rotate(180deg)";
});

const inputs = document.querySelectorAll('.input-container input');
const selects = document.querySelectorAll('.input-container select');
const clearBtns = document.querySelectorAll('.input-container .clear-btn');

const inputDateStart = document.getElementById('id_start_date');
const inputDateEnd = document.getElementById('id_end_date');
const clearBtnDateStart = document.getElementById('clear-start-date');
const clearBtnDateEnd = document.getElementById('clear-end-date');

const inputDates = [inputDateStart, inputDateEnd];
const clearBtnDates = [clearBtnDateStart, clearBtnDateEnd];

function toggleClearBtn(input, clearBtn) {
    if (input.value) {
        clearBtn.style.display = 'block';
    } else {
        clearBtn.style.display = 'none';
    }
}

function clearInput(input, clearBtn) {
    input.value = '';
    toggleClearBtn(input, clearBtn);
}

window.onload = function () {
    const clearBtnAll = document.getElementById('clear-all');
    clearBtnAll.addEventListener('click', () => {
        inputs.forEach((input, index) => {
            const clearBtn = clearBtns[index];
            clearInput(input, clearBtn);
        });
        selects.forEach((select) => {
            select.value = "";
        })
        inputDates.forEach((input) => {
            input.value = "";
        })
    });

    inputs.forEach((input, index) => {
        const clearBtn = clearBtns[index];
        toggleClearBtn(input, clearBtn);
        input.addEventListener('input', () => toggleClearBtn(input, clearBtn));
        clearBtn.addEventListener('click', () => clearInput(input, clearBtn));
    });

    inputDates.forEach((input, index) => {
        const clearBtnDate = clearBtnDates[index];
        input.addEventListener('input', () => {
            clearBtnDate.style.display = 'block';
        });
        if (clearBtnDate) {
            clearBtnDate.addEventListener('click', () => {
                input.value = '';
                clearBtnDate.style.display = 'none';
            });
        }
    })

}

