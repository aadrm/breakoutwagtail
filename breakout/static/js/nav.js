var elements = document.getElementsByClassName("nav-link");

var collapseNav = function() {
    document.getElementById("nav-toggle").checked = false;
};


window.addEventListener('load', function() {
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', collapseNav, false);
    }
});
    