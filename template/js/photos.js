
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
  { src: "./photos/my_home_top.jpg", alt:"Chapra"},
  { src: "./photos/bhagalpur_new.jpg", alt: "Bhagalpur 11:11" },
  { src: "./photos/img_1.jpg", alt: "Bhagalpur 11:11" },
  { src: "./photos/img_2.jpg", alt: "Purnea V - Mart" },
  { src: "./photos/img_3.jpg", alt: "Purnea Polytechic Chowk" },
  { src: "./photos/img_4.jpg", alt: "G P Bhagalpur" },
  { src: "./photos/img_5.jpg", alt: "Mithla Purnea" },
  { src: "./photos/img_6.jpg", alt: "Hackathon 2024" },
  { src: "./photos/img_7.jpg", alt: "Mithla Purnea" },
  { src: "./photos/img_8.jpg", alt: "G P Bhagalpur" },
  { src: "./photos/img_9.jpg", alt: "Realme Service Center" },
  { src: "./photos/img_10.jpg", alt: "Chapra" },
  { src: "./photos/img_11.jpg", alt: "Chapra" },
  { src: "./photos/img_13.jpg", alt: "G P Purnea" },
  { src: "./photos/img_14.jpg", alt: "Purnea Polytechic Chowk" },
  { src: "./photos/img_15.jpg", alt: "Purnea Polytechic Chowk" },
  { src: "./photos/img_16.jpg", alt: "Purnea Polytechic Chowk" },
  { src: "./photos/img_17.jpg", alt: "Purnea Polytechic Chowk" },
  { src: "./photos/img_18.jpg", alt: "G P Purnea" },
  { src: "./photos/img_19.jpg", alt: "Sonpur" },
  { src: "./photos/img_20.jpg", alt: "Gujarat" },
  { src: "./photos/PXL_20250405_145212246.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_150023699.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_150331942.PORTRAIT.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_150532389.PORTRAIT.ORIGINAL.jpg", alt: "Mandar Hill" },
  { src: "./photos/img_21.jpg", alt: "Gujarat" },
  { src: "./photos/PXL_20250405_153522272.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_153544179.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_153747287.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_153825202.jpg", alt: "Mandar Hill" },
  { src: "./photos/PXL_20250405_154644367.jpg", alt: "Mandar Hill" },
  { src: "./photos/IMG-20250709-WA0016.jpg", alt: "Gujarat" },
  { src: "./photos/IMG-20250709-WA0017.jpg", alt: "Gujarat" },
  { src: "./photos/new3.jpg", alt: "Chapra" },
  { src: "./photos/IMG-20250709-WA0018.jpg", alt: "Gujarat" },
  { src: "./photos/brothers.jpg", alt: "Chhath Puja 2025" },
  { src: "./photos/haridwar_love.jpg", alt: "Haridwar Station" },
  { src: "./photos/oldimg.jpg", alt: "Punrea" },
  { src: "./photos/frdm1.jpeg", alt: "Gujarat" },
  { src: "./photos/frdm.jpeg", alt: "Gujarat" },
  { src: "./photos/mukeshpersonal.jpg", alt: "Roommate." }
];

const imageGrid = document.getElementById("imageGrid");

images.forEach(imgData => {
  const wrapper = document.createElement("div");
  wrapper.className = "image-item";

  const img = document.createElement("img");
  img.src = imgData.src;
  img.alt = imgData.alt;
  img.classList.add("img");
  img.loading = "lazy";
  img.onclick = () => openModal(imgData.src);

  const info = document.createElement("div");
  info.className = "image-info";
  info.innerText = imgData.alt; 

  wrapper.appendChild(img);
  wrapper.appendChild(info);
  imageGrid.appendChild(wrapper);
});

// Modal functions
function openModal(src) {
  document.getElementById("imageModal").style.display = "flex";
  document.getElementById("modalImage").src = src;
}

function closeModal() {
  document.getElementById("imageModal").style.display = "none";
}


