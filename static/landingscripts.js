const swiper = new Swiper('.swiper', {
  // Optional parameters
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  //direction: 'vertical',
  loop: true,
  
  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
  
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  
  // And if we need scrollbar
  // scrollbar: {
  // el: '.swiper-scrollbar',
  //},
  });
  

  
  
  
  
  
  document.addEventListener("DOMContentLoaded", function() {
    var kindItems = document.querySelectorAll('.dropdown');
    
    kindItems.forEach(function(kindItem) {
      var submenu = kindItem.querySelector('.submenu');
      
      kindItem.addEventListener("click", function() {
        // Toggle the display property of the submenu when the kind is clicked
        if (submenu.style.display === "none" || submenu.style.display === "") {
          submenu.style.display = "block";
        } else {
          submenu.style.display = "none";
        }
      });
    });
  
    document.getElementById("menu-icon").addEventListener("click", function() {
      var menu = document.getElementById("menu");
      // Toggle the menu's display property
      if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
      } else {
        menu.style.display = "none";
      }
    });
  });