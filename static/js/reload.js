console.log('runs');
window.addEventListener("pageshow", function() {
    console.log('event added');
    if (window.performance.navigation.type == 2){
        console.log('reload')
        location.reload();
    }


})

// location.reload();


// window.onbeforeunload = function () {
//     console.log('reloadcalled');
//     console.log(perfEntries)
//     if (perfEntries.length > 0) {
//         if (perfEntries[0].type === "back_forward") {
//             console.log('reload');
//             location.reload();
//         }

//     }
// };
