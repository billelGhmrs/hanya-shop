

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

function openProductOverlay(description, imageSrc) {
  const overlay = document.getElementById("product-overlay");
  const overlayContent = document.getElementById("overlay-content");
  const productImage = document.getElementById("product-image");
  const productDescription = document.getElementById("product-description");

  productImage.src = imageSrc; // Set the image source
  productDescription.textContent = description; // Set the product description

  overlay.style.display = "block"; // Show the overlay
}

function closeProductOverlay() {
  const overlay = document.getElementById("product-overlay");

  overlay.style.display = "none"; // Hide the overlay
}





function toggleDescription(link) {
  const moreText = link.parentElement.querySelector('.more-text');

  if (moreText.style.display === "none") {
      moreText.style.display = "inline";
      link.innerHTML = "Read less";
  } else {
      moreText.style.display = "none";
      link.innerHTML = "Read more";
  }
}


function searchOnEnter(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); // Prevent the default form submission

    var searchInput = document.getElementById('search-input').value;
    
    // Create a FormData object to send the data
    var formData = new FormData();
    formData.append('query', searchInput);

    fetch('/search', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        // Handle the response from Flask here
        console.log('Search results:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
}

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



const phoneIcon = document.getElementById("phone-icon");
        const phoneDisplay = document.getElementById("phone-display");

        // Add a click event listener to the phone icon
        phoneIcon.addEventListener("click", function () {
            // Toggle the visibility of the phone number
            if (phoneDisplay.style.display === "none") {
                phoneDisplay.style.display = "block";
            } else {
                phoneDisplay.style.display = "none";
            }
        });