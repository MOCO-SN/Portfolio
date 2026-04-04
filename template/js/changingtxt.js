 const texts = [
        { text: "a Developer", color: "#4ade80" },
      //  { text: "a Designer", color: "#60a5fa" },
        { text: "a Gamer", color: "#fc0000ff" },
        { text: "a Creator", color: "#facc15" },
        //{ text: "an Editor", color: "#fb7185" }
    ];

    let index = 0;
    const changeText = document.querySelector(".change-text");

    setInterval(() => {
        index = (index + 1) % texts.length;

        // fade out
        changeText.style.opacity = 0;

        setTimeout(() => {
            changeText.textContent = texts[index].text;
            changeText.style.color = texts[index].color;

            // fade in
            changeText.style.opacity = 1;
        }, 500);

    }, 2000); // Change every 2 seconds