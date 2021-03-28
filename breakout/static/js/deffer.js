"use strict";

function loadDeferredIframe() {
    console.log('loading-iframe');
    if(this.getAttribute('data-src')) {
        this.setAttribute('src',this.getAttribute('data-src'));
        this.removeEventListener('click', loadDeferredIframe, false)
        this.removeEventListener('mouseover', loadDeferredIframe, false)

    } 
};



window.addEventListener('load', function() {
    console.log('loaded')
    let iframes = document.getElementsByClassName('js-iframe-defer')
    for (var i = 0; i < iframes.length; i++) {
        iframes[i].addEventListener('click', loadDeferredIframe);
        iframes[i].addEventListener('mouseover', loadDeferredIframe, false);
    }
});
    