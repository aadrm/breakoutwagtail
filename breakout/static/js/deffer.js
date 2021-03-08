function loadDeferredIframes() {
    console.log('load...');
    var vidDefer = document.getElementsByTagName('iframe');
    for (var i=0; i<vidDefer.length; i++) {
        if(vidDefer[i].getAttribute('data-src')) {
            vidDefer[i].setAttribute('src',vidDefer[i].getAttribute('data-src'));
            console.log('...loaded');
        } 
    } 
};

window.addEventListener('load', function() {
    console.log('prepared_defer')
    loadDeferredIframes();
});