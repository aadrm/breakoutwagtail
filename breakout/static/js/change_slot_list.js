window.addEventListener('load', function() {
    addOnclick();
});

function addOnclick() {
    console.log('added')
    buttons = document.getElementsByClassName('js-button-change-slot');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].onclick = showSlots
    } 

}


function closeList() {
    let responseElement = document.getElementsByClassName('js-change-slot-response')[0];
    responseElement.remove();
}

function showSlots() {
    console.log('show called')
    var currentslot = this.dataset.currentslot;
    var frompage = this.dataset.frompage;
    var order = this.dataset.order;
    var cartItem = this.dataset.cartitem;
    var customer = this.dataset.customer;
    var posturl = this.dataset.posturl;
    console.log(frompage)
    ajaxRequest = new XMLHttpRequest();
    ajaxRequest.open("POST", posturl, true);
    ajaxRequest.responseType = "document";
    ajaxRequest.send(JSON.stringify({
        "currentslot": currentslot,
        "frompage": frompage,
        "order": order,
        "customer": customer,
        "cartitem": cartItem,
    }));
    ajaxRequest.onreadystatechange = callBackShowSlots;
};

function callBackShowSlots() {
    if (ajaxRequest.readyState == 4) {

        let availableSlots = this.response.getElementsByClassName('js-change-slot-response')[0];
        let body = document.getElementsByTagName('body')[0]
        console.log(availableSlots)
        body.prepend(availableSlots)
    }
};
