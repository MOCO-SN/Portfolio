
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImage');

  // Open modal on image click
  document.querySelectorAll('.img').forEach(img => {
    img.addEventListener('click', () => {
      modal.style.display = 'flex';
      modalImg.src = img.src;
    });
  });

  // Close modal on background click
  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target.classList.contains('close')) {
      closeModal();
    }
  });

  // Close modal on ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
    }
  });

  function closeModal() {
    modal.style.display = 'none';
    modalImg.src = '';
  }

const images = [
  { src: "./photos/my_home_top.jpg", alt:"img top"},
  { src: "./photos/bhagalpur_new.jpg", alt: "Image 1" },
  { src: "./photos/img_1.jpg", alt: "Image 2" },
  { src: "./photos/img_2.jpg", alt: "Image 3" },
  { src: "./photos/img_3.jpg", alt: "Image 4" },
  { src: "./photos/img_4.jpg", alt: "Image 5" },
  { src: "./photos/img_5.jpg", alt: "Image 6" },
  { src: "./photos/img_6.jpg", alt: "Image 7" },
  { src: "./photos/img_7.jpg", alt: "Image 8" },
  { src: "./photos/img_8.jpg", alt: "Image 9" },
  { src: "./photos/img_9.jpg", alt: "Image 10" },
  { src: "./photos/img_10.jpg", alt: "Image 11" },
  { src: "./photos/img_11.jpg", alt: "Image 12" },
  { src: "./photos/img_13.jpg", alt: "Image 13" },
  { src: "./photos/img_14.jpg", alt: "Image 14" },
  { src: "./photos/img_15.jpg", alt: "Image 15" },
  { src: "./photos/img_16.jpg", alt: "Image 16" },
  { src: "./photos/img_17.jpg", alt: "Image 17" },
  { src: "./photos/img_18.jpg", alt: "Image 18" },
  { src: "./photos/img_19.jpg", alt: "Image 19" },
  { src: "./photos/img_20.jpg", alt: "Image 20" },
  { src: "./photos/PXL_20250405_145212246.jpg", alt: "Image 21" },
  { src: "./photos/PXL_20250405_150023699.jpg", alt: "Image 22" },
  { src: "./photos/PXL_20250405_150331942.PORTRAIT.jpg", alt: "Image 23" },
  { src: "./photos/PXL_20250405_150532389.PORTRAIT.ORIGINAL.jpg", alt: "Image 24" },
  { src: "./photos/img_21.jpg", alt: "Image 25" },
  { src: "./photos/PXL_20250405_153522272.jpg", alt: "Image 26" },
  { src: "./photos/PXL_20250405_153544179.jpg", alt: "Image 27" },
  { src: "./photos/PXL_20250405_153747287.jpg", alt: "Image 28" },
  { src: "./photos/PXL_20250405_153825202.jpg", alt: "Image 29" },
  { src: "./photos/PXL_20250405_154644367.jpg", alt: "Image 30" },
  { src: "./photos/IMG-20250709-WA0016.jpg", alt: "Image 31" },
  { src: "./photos/IMG-20250709-WA0017.jpg", alt: "Image 32" },
  { src: "./photos/new 3.jpg", alt: "Image 33" },
  { src: "./photos/IMG-20250709-WA0018.jpg", alt: "Image 33" }
];

const imageGrid = document.getElementById("imageGrid");

images.forEach(imgData => {
  const img = document.createElement("img");
  img.src = imgData.src;
  img.alt = imgData.alt;
  img.classList.add("img");
  img.loading = "lazy";
  img.onclick = () => openModal(imgData.src);
  imageGrid.appendChild(img);
});

// Modal functions
function openModal(src) {
  document.getElementById("imageModal").style.display = "flex";
  document.getElementById("modalImage").src = src;
}

function closeModal() {
  document.getElementById("imageModal").style.display = "none";
}