let ws = new WebSocket("wss://HOST IP:12345/");

slider1 = document.querySelector("#slider1")
slider1.oninput = function() {
    ws.send(`a${this.value}`)
}
slider2 = document.querySelector("#slider2")
slider2.oninput = function() {
    ws.send(`b${this.value}`)
}

sliderFOV = document.querySelector("#sliderFOV")
sliderFOV.oninput = function() {
    if (this.value == 1) {
        ws.send(`f${this.value}`)
    } else if (this.value == 100) {
        ws.send(`f${this.value}`)
    } else if (this.value == 2) {
        ws.send(`f${this.value}`)
    } else if (this.value == 99) {
        ws.send(`f${this.value}`)
    }
}


function lookLeft() {
    ws.send(`lookLeft`)
}

function lookRight() {
    ws.send(`lookRight`)
}

function F1(){
    ws.send(`F1`)
}

function T() {
    ws.send(`T`)
}

rightPovorotnikButton = document.querySelector("#rightPovorotnik")
rightPovorotnikButton.onclick = function() {
    ws.send(`rightPovorotnik`)
}

lookRightButton = document.querySelector("#lookRight")
lookRightButton.onclick = function() {
    ws.send(`lookRight`)
}

function getAccel(){
    permsButton = document.querySelector("#accelPermsButton");
    permsButton.classList.toggle("hide")

    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            function handleMotionEvent(event) {
                const y = event.accelerationIncludingGravity.y;
                ws.send(`${y}`)
            }

            window.addEventListener("devicemotion", handleMotionEvent, true);
        }
    });
}