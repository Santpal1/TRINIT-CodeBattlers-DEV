document.addEventListener("DOMContentLoaded", function () {
    const textElement = document.querySelector('.typing-text');
    const linesToType = [
        "Learn", "Practice", "Succeed"
    ];

    let lineIndex = 0;
    let charIndex = 0;

    function typeText() {
        textElement.textContent = linesToType[lineIndex].substring(0, charIndex);
        charIndex++;

        if (charIndex <= linesToType[lineIndex].length) {
            setTimeout(typeText, 100); 
        } else {
            setTimeout(eraseText, 1000); 
        }
    }

    function eraseText() {
        charIndex--;

        if (charIndex >= 0) {
            textElement.textContent = linesToType[lineIndex].substring(0, charIndex);
            setTimeout(eraseText, 50); 
        } else {
            lineIndex = (lineIndex + 1) % linesToType.length; 
            setTimeout(typeText, 500); 
        }
    }

    setTimeout(typeText, 1000); 
});