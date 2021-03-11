"use strict";

window.addEventListener('load',function() {
    startTimers();
    setInterval(function(){
        startTimers();
    }, 1000);
});



var urls = document.getElementById("js-urls")
var itemsUrl = urls.dataset.item;
var couponsUrl = urls.dataset.coupon;
var invoiceUrl = urls.dataset.invoice;


function startTimers() {
    let items = document.getElementsByClassName("js-cart-item");
    let timers = document.getElementsByClassName("js-expiry-counter");
    let newTime;
    let prefix;
    let timeRemaining;

    if (items.length) {
        if (timers.length) {
            prefix = timers[0].dataset.prefix;
            let expire = false;
            for (let i = 0; i < timers.length; i++) {
                newTime = parseInt(timers[i].dataset.remaining) - 1; 
                if (newTime <= 0 || isNaN(newTime)) {
                    newTime = 0;
                }
                let minutes = Math.floor(newTime / 60);
                let seconds = newTime % 60;
                minutes = padNumber(minutes, 2);
                seconds = padNumber(seconds, 2);

                timeRemaining = prefix + minutes + ":" + seconds;
                timers[i].textContent = timeRemaining;
                timers[i].dataset.remaining = newTime;
                if (!expire) {
                    if (newTime == 0) {
                        expire = true;
                        displayCartError();
                    }
                } 
            }
        }
    } else {
        displayCartError();
    }
};

function padNumber(n, width) {
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(0) + n;;

};

//
// Remove Item
//

var itemListWrapper = document.getElementById('js-item-list-wrapper');

function refreshItem() {
    xhr = new XMLHttpRequest();
    xhr.open("POST", itemsUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"refresh": true}));
    xhr.parent = this;
    xhr.onreadystatechange = itemListCallback;
}

function removeItem(e) {
    console.log('remove item')
    xhr = new XMLHttpRequest();
    xhr.open("POST", itemsUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"item": e.dataset.item, "cart": e.dataset.cart}));
    xhr.parent = this;
    xhr.onreadystatechange = itemListCallback;
}

function itemListCallback() {
   if(xhr.readyState == 4) {
        let parser = new DOMParser ();
        let responseDoc = parser.parseFromString(this.responseText, "text/html");
        itemsInCartDiv = responseDoc.getElementById('js-items-in-cart');
        itemListWrapper.firstElementChild.remove();
        itemListWrapper.appendChild(itemsInCartDiv);
        // function in different file
        refreshInvoice();
        changeInCheckoutForm();
        // if (refresh){
        //     refreshCoupon();
        // }
    }
}

//
// Coupons Handling
//

var applyCouponButton = document.getElementById("js-apply-coupon-button");
var couponListWrapper = document.getElementById("js-coupon-list-wrapper");
var invoiceDetailsDiv = document.getElementById("js-invoice-div");

function applyCoupon() {
    codeField = document.getElementById("id_code") // id dependant on django form name
    code = codeField.value;
    xhr = new XMLHttpRequest();
    xhr.open("POST", couponsUrl, true);
    // xhr.open("POST", this.applyCouponButton.dataset.applycouponurl, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // xhr.responseType = "document";
    xhr.send(JSON.stringify({"code": code}));
    xhr.parent = this;
    xhr.onreadystatechange = couponListCallback;
};

function removeCoupon(e) {
    xhr = new XMLHttpRequest();
    xhr.open("POST", couponsUrl, true);
    // xhr.open("POST", e.dataset.removecouponurl, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"cart_coupon": e.dataset.coupon, "cart": e.dataset.cart}));
    xhr.parent = this;
    xhr.onreadystatechange = couponListCallback;
};

function refreshCoupon() {
    xhr = new XMLHttpRequest();
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({"refresh": true}));
    xhr.parent = this;
    xhr.onreadystatechange = couponListCallback;
};

function couponListCallback() {
   if(xhr.readyState == 4) {
        let parser = new DOMParser ();
        let responseDoc = parser.parseFromString(this.responseText, "text/html");
        couponsInCartDiv = responseDoc.getElementById('js-coupons-in-cart');
        couponListWrapper.firstElementChild.remove();
        couponListWrapper.appendChild(couponsInCartDiv);
        // if (refresh){
        refreshItem();
        // }
    }
};

function refreshInvoice() {
    xhr = new XMLHttpRequest();
    xhr.open("POST", invoiceUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.parent = this;
    xhr.send();
    xhr.onreadystatechange = invoiceCallback;
};

function invoiceCallback() {
   if(xhr.readyState == 4) {
        let parser = new DOMParser ();
        let responseDoc = parser.parseFromString(this.responseText, "text/html");
        invoiceResponse = responseDoc.getElementById('js-invoice-response');
        try {
            invoiceDetailsDiv.firstElementChild.remove();
        } finally {
            invoiceDetailsDiv.appendChild(invoiceResponse);
        }
    }
};


//
// Empty cart | expired items
//

var cartValid = true;
var cartError = document.getElementById("js-cart-error");

function displayCartError() {
    if (cartValid == true) {
        cartValid = false;
        invoiceDetails = document.getElementById("js-invoice-details");
        invoiceDetails.remove();
        cartError.classList.remove("u-visually-hidden");
    }
};