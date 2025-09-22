const familyData = [
  { src: "/slide_images/unknown_male.png", title: "My Grandfather", name: "Maheshwar Singh" },
  { src: "/slide_images/unknown_female.png", title: "My Grandmother", name: "Sakuntla Devi" },
  { src: "/slide_images/unknown_female.png", title: "My Maternal Grandmother", name: "Sujanti Uraw" },
  { src: "/slide_images/unknown_male.png", title: "My Father", name: "Manoj Kumar Singh" },
  { src: "/slide_images/unknown_female.png", title: "My Mother", name: "Veena Devi" },
  { src: "/slide_images/unknown_male.png", title: "My Elder Brother", name: "Shekhar Patel" },
  { src: "/slide_images/unknown_female.png", title: "My Younger Sister", name: "Shilpi Kumari" },
  { src: "/slide_images/unknown_female.png", title: "My Younger Sister", name: "Soni Kumari" },
  { src: "/slide_images/unknown_male.png", title: "My Younger Brother", name: "Prince Patel" }
];

const familyWrapper = document.getElementById("familyWrapper");

familyData.forEach(member => {
  const container = document.createElement("div");

  const img = document.createElement("img");
  img.src = member.src;
  img.alt = "img";
  img.classList.add("img-supported");
  img.loading = "lazy";

  const details = document.createElement("div");
  details.classList.add("details");

  const title = document.createElement("h4");
  title.textContent = member.title;

  const name = document.createElement("p");
  name.textContent = member.name;

  details.appendChild(title);
  details.appendChild(name);
  container.appendChild(img);
  container.appendChild(details);
  familyWrapper.appendChild(container);
});

// Image slider
const imageWrapper = document.querySelector('.wrapper-supported');
const imageItems = document.querySelectorAll('.wrapper-supported > *');
const imageLength = imageItems.length;
const perView = 3;
let totalScroll = 0;
const delay = 2000;
let autoScroll;

imageWrapper.style.setProperty('--per-view', perView);

// Duplicate first items for smooth infinite scroll
for (let i = 0; i < perView; i++) {
  imageWrapper.insertAdjacentHTML('beforeend', imageItems[i].outerHTML);
}

// Start scrolling
function startAutoScroll() {
  autoScroll = setInterval(scrolling, delay);
}

// Stop scrolling
function stopAutoScroll() {
  clearInterval(autoScroll);
}

function scrolling() {
  totalScroll++;
  if (totalScroll === imageLength + 1) {
    stopAutoScroll();
    totalScroll = 1;
    imageWrapper.style.transition = '0s';
    imageWrapper.style.left = '0';
    startAutoScroll();
  }
  const widthEl = document.querySelector('.wrapper-supported > :first-child').offsetWidth + 24;
  imageWrapper.style.left = `-${totalScroll * widthEl}px`;
  imageWrapper.style.transition = '.2s';
}

// Hover events to pause/resume
imageWrapper.addEventListener("mouseenter", stopAutoScroll);
imageWrapper.addEventListener("mouseleave", startAutoScroll);

// Start initially
startAutoScroll();
