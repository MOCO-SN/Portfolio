document.addEventListener("DOMContentLoaded", function() {
    var overlays = document.getElementById("overlays");
    var okBtn = document.getElementById("okBtn");
    var updateBtn = document.getElementById("updateBtn");

    // Function to handle OK button click
    okBtn.addEventListener("click", function() {
        overlays.style.display = "none";
        // window.location.href = "index.html";
    });

    // Function to handle Update button click
    updateBtn.addEventListener("click", function() {
        // Redirect user to the update URL
        window.location.href = "https://www.instagram.com/_sachin_2006_01/";
    });

    // Show the overlay on startup
    overlays.style.display = "block";
    
});