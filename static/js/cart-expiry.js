window.onload = function() {
    console.log('set timers');
    startTimers();
    setInterval(function(){
        startTimers();
    }, 1000);
}

function startTimers() {
    let timers = document.getElementsByClassName("js-expiry-counter")
    let newTime;
    let prefix;
    let timeRemaining;
    prefix = timers[0].dataset.prefix

    console.log(timers.length)
    for (i = 0; i < timers.length; i++) {
        newTime = parseInt(timers[i].dataset.remaining) - 1; 
        if (newTime <= 0 || isNaN(newTime)) {
            newTime = 0;
        }
        minutes = Math.floor(newTime / 60);
        seconds = newTime % 60;
        minutes = padNumber(minutes, 2);
        seconds = padNumber(seconds, 2);

        timeRemaining = prefix + minutes + ":" + seconds;
        timers[i].textContent = timeRemaining;
        timers[i].dataset.remaining = newTime;
    }
};

function padNumber(n, width) {
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join(0) + n;;

};
