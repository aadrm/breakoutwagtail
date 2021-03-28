"use strict";

function loadDeferredIframe(e) {
    console.log('loading-iframe');
    if(e.getAttribute('data-src')) {
        e.setAttribute('src',e.getAttribute('data-src'));
        e.setAttribute('onmouseover', '');
    } 
};
