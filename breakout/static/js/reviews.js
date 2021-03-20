"use strict";

window.addEventListener('load',function() {
    var current = 0;
    var reviews = document.getElementsByClassName('review');
    var last = reviews.length - 1;
    console.log(reviews.length > 0);
    setInterval(function(){
        console.log('log')
        nextReview();
    }, 7000);

    function nextReview() {
        console.log(current);
        reviews.item(current).classList.remove('review-show');
        if (current < last) {
            current +=1;
        } else {
            current = 0;
        }

        reviews.item(current).classList.add('review-show');
    };
});


