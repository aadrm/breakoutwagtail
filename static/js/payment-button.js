window.addEventListener('load', function() {
    console.log(disabledButton)
    changeInCheckoutForm();
});

var disabledButton = document.getElementById('js-disabled-button')
var errMsg
var fillFlag;
var emailFlag;
var paymentFlag;
var termsFlag;

function changeInCheckoutForm() {
    resetMessageFlags()
    console.log('change detected')
    let checkoutForm = document.getElementById('js-checkout-form');
    let buttonDiv = document.getElementById('js-checkout-button-div');
    let paymentMethod = getRadiosValue()
    console.log(paymentMethod)
    let emailok = false;
    // checkCartPrice();
    emailok = validateemail();
    console.log(emailok);
    buttonDiv.innerHTML = "";
    buttonDiv.appendChild(disabledButton);
    if (isRequiredFilled(checkoutForm) && emailok) {
        loadPaymentButton(checkoutForm, buttonDiv, paymentMethod);
    }
    errorMessage();
};

function loadPaymentButton(checkoutForm, buttonDiv, paymentMethod) {
    let request
    let params = "payment=" + paymentMethod
    request = new XMLHttpRequest();
    request.open("GET", checkoutForm.dataset.url + "?" + params, true)
    request.responseType = "document";
    request.send();
    request.onreadystatechange = function(self) {
        if(request.readyState == 4) {
            childrenToAdd = this.response.body.children
            console.log(childrenToAdd)
            buttonDiv.innerHTML = "";
            for (let i = 0; i < childrenToAdd.length; i++) {
                console.log(childrenToAdd[i])
                buttonDiv.appendChild(childrenToAdd[i])
            }
        }
    }

};

function validateemail() {  
    var x=document.getElementById('id_email').value;  
    var atposition=x.indexOf("@");  
    var dotposition=x.lastIndexOf(".");  
    if (atposition<1 || dotposition<atposition+2 || dotposition+2>=x.length){  
        emailFlag = true;
        return false;  
    } else {
        return true;
    }
}  ;

function isRequiredFilled(form) {
    let requiredFields = form.querySelectorAll("[required]");
    let allAreFilled = true;
    let radioCheck = false;
    requiredFields.forEach(
        function(i) {
            if (i.type === "radio") {
                console.log('radiocheck')
                if (i.checked) {
                    radioCheck = true;
                    paymentFlag = false;
                }
            }
            if (i.type === "checkbox") {
                if (!i.checked) {
                    allAreFilled = false;
                    termsFlag = true;
                }
            }
            if (!i.value) {
                console.log('not all filled')
                allAreFilled = false;
                fillFlag = true;
            }
        }
    )
    if (allAreFilled && radioCheck) {
        return true;
    } else {
        return false;
    }
};

function getRadiosValue() {
    let radios = document.getElementsByName('payment')
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i].value
        }
    }
};

function errorMessage() {
    console.log('errorMessages')
    errMsg = disabledButton.dataset.msgfill;
    disabledButton.innerText = errMsg;
    if (fillFlag) {
        errMsg = disabledButton.dataset.msgfill;
    } else if (emailFlag) {
        errMsg = disabledButton.dataset.msgemail;
    } else if (paymentFlag) {
        errMsg = disabledButton.dataset.msgpayment;
    } else if (termsFlag) {
        errMsg = disabledButton.dataset.msgterms;
    } else {
        errMsg = disabledButton.dataset.msgwait;
    }
    disabledButton.innerText = errMsg;
};

function resetMessageFlags() {
    fillFlag = false;
    emailFlag = false;
    paymentFlag = true;
    termsFlag = false;
};
// function checkCartPrice() {
//     let priceElement = document.getElementById('js-price');
//     let checkoutForm = document.getElementById('js-checkout-form');
//     price = priceElement.dataset.price;
//     if (price >= 0){

//     }
//     return price;
// }