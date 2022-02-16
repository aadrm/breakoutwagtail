var today = new Date();
var defaultYear = today.getFullYear();
var defaultMonth = today.getMonth() + 1;
var lastClickedId = 'last-clicked';
var lastClickedCellId = 'cell--last-clicked';
var ajaxRequest;
var calendarLoadingWindow = [];
var loadedCalendar = [];
var availableSpinner = createAvailableSpinner();
var calendarSpinner = createCalendarSpinner();
var bookingFormSpinner =createBookingFormSpinner();
var calendarList = new Array();

window.addEventListener('load', function() {
    console.log('running')
    availableSpinner.style.display ="table-row";
    availableSpinner.remove();
    document.body.appendChild(bookingFormSpinner);
    initialiseCalendars();
});


function initialiseCalendars() {
    calendarFrames = document.getElementsByClassName("js-calendar-window");
    for (i = 0; i < calendarFrames.length; i++) {
        calendarList[i] = new Calendar(calendarFrames[i], i);
    }
};

class Calendar { 
    constructor(frame, index) {
        this.frame = frame;
        this.index = index;
        this.frame.appendChild(calendarSpinner.cloneNode(true));
        this.calendarData;
        this.loadCalendar();
    }

    loadCalendar(year = defaultYear, month = defaultMonth) {
        this.frame.getElementsByClassName("calendar-spinner")[0].style.display = "block";
        let request
        let room = this.frame.dataset.room;
        let params = "room=" + room + "&year=" + year + "&month=" + month;
        request = new XMLHttpRequest();
        request.open("GET", this.frame.dataset.url + "?" + params, true)
        request.responseType = "document";
        request.send();
        request.parent = this;
        request.onreadystatechange = function(self) {
            if(request.readyState == 4) {
                this.parent.calendarData = this.response.getElementsByClassName('calendar')[0];
                this.parent.updateCalendar();
                this.parent.hideSpinner();
                this.parent.frame.style.height = "100%";
                this.parent.addEventToCalendarNav();
                this.parent.addEventToDay();
            }
        }

    }

    navigateCalendar(year, month) {
        // disableNav();
        if (year && month) {
            this.loadCalendar(year, month);
        } else {
            this.loadCalendar();
        }
    };

    addEventToCalendarNav() {
        let navButtons = this.frame.getElementsByClassName("js-cal-button")
        for (i = 0; i < navButtons.length; i++) {
            let year = parseInt(navButtons[i].dataset.year);
            let month = parseInt(navButtons[i].dataset.month);
            navButtons[i].addEventListener("click", () => {
                this.navigateCalendar(year, month);
            }, false);
        }
    }

    addEventToDay() {
        let available = this.frame.getElementsByClassName("js-day");

        for (i = 0; i < available.length; i++) {
            available[i].addEventListener("click", showSessionsOnDay);
        }
    }

    updateCalendar() {
        let calendar = this.frame.getElementsByClassName('calendar');
        for(let i = 0; i < calendar.length; i++) {
            calendar[i].remove();
        }
        this.frame.appendChild(this.calendarData);
    }

    hideSpinner() {

        this.frame.getElementsByClassName("calendar-spinner")[0].style.display = "none";
    }

}

function showSessionsOnDay() {
    let lastClicked = document.getElementById(lastClickedId);
    let availableSlots = document.getElementsByClassName('available-slots-response')[0]

    if(lastClicked) {
        lastClicked.removeAttribute('id');
    }

    if(availableSlots) {
        availableSlots.remove();
    }

    dataYear = (this.dataset.year);
    dataMonth = (this.dataset.month);
    dataDay = (this.dataset.day);
    dataRoom = (this.dataset.room);
    params = "year=" + dataYear + "&month=" + dataMonth + "&day=" + dataDay + "&room=" + dataRoom
    this.id = "last-clicked";
    markLastClickedCell();
    let siblingRow = getLastClickedRow();
    insertAfter(availableSpinner, siblingRow)
    ajaxRequest = new XMLHttpRequest();
    ajaxRequest.open("GET", this.dataset.url + "?" + params  , true);
    ajaxRequest.responseType = "document";
    ajaxRequest.send();
    ajaxRequest.onreadystatechange = callBackAvailability;
};

function showBookingForm() {
    bookingFormSpinner.style.display = "block";
    slot = this.dataset.slot;
    ajaxRequest = new XMLHttpRequest();
    params = "slot=" + this.dataset.slot
    ajaxRequest.open("GET", this.dataset.bookingurl + "?" + params  , true);
    ajaxRequest.responseType = "document";
    ajaxRequest.send();
    ajaxRequest.onreadystatechange = callBackSlotForm;
};

function callBackAvailability() {
    if (ajaxRequest.readyState == 4) {
        let availableSlots = this.response.getElementsByClassName('available-slots-response')[0];
        let siblingRow = getLastClickedRow();
        availableSpinner.remove();
        insertAfter(availableSlots, siblingRow);
        addEventToSlot();
    }
};

function callBackSlotForm() {
    if (ajaxRequest.readyState == 4) {
        console.log('being called')
        let form = this.response.getElementsByClassName('booking-form-response')[0];
        let body = document.getElementsByTagName('body')[0];
        // if (!form == 'undefined') {
            body.prepend(form);
            addEventCloseForm();
            bookingFormSpinner.style.display = "none";
        // } else {
            bookingFormSpinner.style.display = "none";
        // }
    }
};

function closeBookingForm() {
    form = document.getElementsByClassName("booking-form-response")[0];
    form.remove();
}

function addEventCloseForm() {
    elements = document.getElementsByClassName('js-close-onclick');
    for (i = 0; i < elements.length; i++) {
        elements[i].addEventListener("click", closeBookingForm);
    }
};

function disableNav() {
    let navButton = document.getElementsByClassName("js-cal-button")
    for (i = 0; i < navButton.length; i++) {
        navButton[i].removeEventListener("click", navigateCalendar);
    }
}


function addEventToDay() {
    let available = document.getElementsByClassName("js-day");

    for (i = 0; i < available.length; i++) {
        console.log('added')
        available[i].addEventListener("click", showSessionsOnDay);
    }
}

function addEventToSlot() {
    let slots = document.getElementsByClassName('js-available-slot');
    for (i = 0; i < slots.length; i++) {
        slots[i].addEventListener("click", showBookingForm);
    }
    slots = document.getElementsByClassName('js-admin-slot__extra-button');
    for (i = 0; i < slots.length; i++) {
        slots[i].addEventListener("click", showBookingForm);
    }
};

function getLastClickedRow(){
    lastClicked = document.getElementById(lastClickedId);
    row = lastClicked.closest(".data-row");
    return row;
};

function markLastClickedCell() {
    lastClickedCell = document.getElementById(lastClickedCellId);
    if (lastClickedCell) {
        lastClickedCell.removeAttribute('id');
    }
    lastClicked = document.getElementById(lastClickedId);
    cell = lastClicked.closest('td');
    cell.id='cell--last-clicked';
};

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
};


//
// html elements
//

// spinner base
function createSpinnerBase () {
    let ldSpinner = document.createElement("div");
    ldSpinner.classList.add("ld-spinner");
    let ldWrapper = document.createElement("div");
    ldWrapper.classList.add("ld-wrapper");
    ldWrapper.appendChild(ldSpinner);
    return ldWrapper;
}

// calendar-spinner
function createCalendarSpinner () {
    let calSpinner = document.createElement("div");
    calSpinner.classList.add("calendar-spinner");
    calSpinner.appendChild(createSpinnerBase());
    return calSpinner;
}

// available slots spinner 
function createAvailableSpinner () {
    let spinnerWrapper = document.createElement("div");
    spinnerWrapper.classList.add("available-spinner__spinner-wrapper");
    let td = document.createElement("td");
    td.colSpan="7";
    let tr = document.createElement("tr")
    tr.classList.add("available-spinner")
    spinnerWrapper.appendChild(createSpinnerBase());
    td.appendChild(spinnerWrapper);
    tr.appendChild(td);
    return tr;
}

function createBookingFormSpinner () {
    let spinnerWrapper = document.createElement("div");
    spinnerWrapper.classList.add("booking-form-spinner");
    spinnerWrapper.appendChild(createSpinnerBase());
    return spinnerWrapper;
}