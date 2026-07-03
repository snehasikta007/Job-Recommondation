// Simple animation effect
window.addEventListener("scroll", function() {
    let cards = document.querySelectorAll(".feature-card");

    cards.forEach(card => {
        let position = card.getBoundingClientRect().top;
        let screen = window.innerHeight;

        if(position < screen - 100){
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }
    });
});