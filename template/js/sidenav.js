let isMenuOpen = false;

function openNav() {
    const sidenav = document.getElementById("mySidenav");
    const menuBtn = document.querySelector(".topnav .menu button");
    
    if (isMenuOpen) {
      // Close the menu
      sidenav.style.width = "0";
      document.body.style.overflow = "auto";
      isMenuOpen = false;
    } else {
      // Open the menu
      sidenav.style.width = "250px";
      document.body.style.overflow = "hidden";
      isMenuOpen = true;
    }
}
  
  function closeNav() {
    const sidenav = document.getElementById("mySidenav");
    sidenav.style.width = "0";
    document.body.style.overflow = "auto";
    isMenuOpen = false;
  }