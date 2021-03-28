"use strict";

window.addEventListener('load', function() {
    addOnclick();
});

function addOnclick() {
    console.log('added')
    let buttons;
    buttons = document.getElementsByClassName('js-button-change-slot');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = showSlots
    } 
    buttons = document.getElementsByClassName('js-button-change-product');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = showSlots
    } 

}


function closeList() {
    let responseElement = document.getElementsByClassName('js-change-response')[0];
    responseElement.remove();
}

function showSlots() {
    var current = this.dataset.current;
    var frompage = this.dataset.frompage;
    var order = this.dataset.order;
    var cartItem = this.dataset.cartitem;
    var customer = this.dataset.customer;
    var posturl = this.dataset.posturl;
    console.log(frompage)
    let xhr = new XMLHttpRequest();
    xhr = new XMLHttpRequest();
    xhr.open("POST", posturl, true);
    xhr.responseType = "document";
    xhr.send(JSON.stringify({
        "current": current,
        "frompage": frompage,
        "order": order,
        "customer": customer,
        "cartitem": cartItem,
    }));
    xhr.onreadystatechange = callBackShowChange;
};

function callBackShowChange() {
    if (this.readyState == 4) {

        let availableSlots = this.response.getElementsByClassName('js-change-response')[0];
        let body = document.getElementsByTagName('body')[0]
        console.log(availableSlots)
        body.prepend(availableSlots)
    }
};
