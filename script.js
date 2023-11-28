function spinWheel() {
    const wheel = document.getElementById('wheel');

    // Disable button during animation
    document.getElementById('spin-btn').disabled = true;

    // Rotate the wheel randomly
    const rotation = 1080 + Math.floor(Math.random() * 360); // Rotate between 1080 and 1440 degrees
    wheel.style.transform = `rotate(${rotation}deg)`;

    // Enable the button after the animation
    setTimeout(() => {
        document.getElementById('spin-btn').disabled = false;
    }, 3000);
}
