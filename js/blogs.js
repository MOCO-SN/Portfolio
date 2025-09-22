const blogs = [
     {
        title: "West Bengal, Bagdora (Airport)",
        author: "Sachin",
        date: "Sept 14, 2025",
        image: "photos/.jpg",
        description: ``
    },
    {
        title: "Kolkata (Airport)",
        author: "Sachin",
        date: "Sept 13, 2025",
        image: "photos/.jpg",
        description: ``
    },
    {
        title: "Delhi, Terminal 3 and Terminal 1(Airport)",
        author: "Sachin",
        date: "Sept 13, 2025",
        image: "photos/.jpg",
        description: ``
    },
    {
        title: "Uttrakhand, Gopeshwar, Chamoli (IT Gopeshwar)",
        author: "Sachin",
        date: "Sept 4, 2025",
        image: "photos/.jpg",
        description: ``
    },
    {
        title: "Uttrakhand, Reshikesh",
        author: "Sachin",
        date: "Sept 3, 2025",
        image: "photos/.jpg",
        description: ``
    },
    {
        title: "Uttrakhand, Dehradunn",
        author: "Sachin",
        date: "Sept 2, 2025",
        image: "photos/.jpg",
        description: ``
    },
        {
        title: "Back to Chapra – My Hometown",
        author: "Sachin",
        date: "Aug 14, 2025",
        image: "photos/my_home_top.jpg",
        description: `After a long time, I finally went back to my hometown, Chapra. 
        It felt amazing to return to the place where so many memories of my childhood and growing-up days were made. 
        Walking through the familiar streets, seeing old friends, and revisiting favorite spots brought back a flood of nostalgia.
        Everything seemed both the same and different—some places had changed, yet the feeling of home remained unchanged. 
        I enjoyed reconnecting with family, sharing stories, and reliving the simple joys that only home can give.
        Going back to Chapra reminded me how special hometowns are. Even after being away for so long, the love, 
        warmth, and memories tied to this place are unforgettable.`
    },
    {
        title: "Trip to Gujarat – Vadodara",
        author: "Sachin",
        date: "Jul 31, 2025",
        image: "./photos/IMG-20250709-WA0016.jpg",
        description: `I recently visited Vadodara, Gujarat and spent an amazing 14 days there with my 7 friends. 
        It was a trip full of laughter, fun, and unforgettable memories. 
        From exploring the beautiful streets of Vadodara to enjoying the local food, every single day was a new adventure.
        We visited popular spots, enjoyed long conversations late into the night, 
        and made countless inside jokes that we’ll remember forever. 
        Whether it was sightseeing, relaxing together, or just walking around the city, 
        the moments we shared made this trip truly special.
        Those 14 days weren’t just a vacation – they were a chapter in our friendship that we’ll always treasure. 
        Vadodara gave us memories for a lifetime, and I can’t wait for our next trip together!`
    },
    {
        title: "Last Day of our college",
        author: "Sachin",
        date: "Jun 27, 2025",
        image: "photos/leaving_my_college.jpg",
        description: `My last day of college was a mix of happiness and sadness. 
        I will never forget all my friends who shared countless memories with me—laughter,
        fun, hard work, and late-night talks.
        I’m deeply thankful to all my teachers for their guidance, support, 
        and the life lessons they gave me beyond the classroom.
        It was my final day there, but it turned out to be one of the greatest days of my life. 
        Even though college life has ended, the friendships and memories will remain in my heart forever.
        The last day of my college was filled with bittersweet memories,
        heartfelt goodbyes, laughter, and tears.
        We cherished every moment,
        knowing it marked the end of a beautiful chapter.`
    },
    {
        title: "Trip to Mandar Hill",
        author: "Sachin",
        date: "April 11, 2025",
        image: "photos/PXL_20250405_154644367.jpg",
        description: `I went on an amazing trip to Mandar Hill with my three friends, 
        and it turned out to be a day full of adventure and peace. Surrounded by nature and fresh air, 
        the place was a perfect escape from our daily routine.
        We climbed the hill, enjoyed the beautiful views, and clicked lots of pictures to capture the moments. 
        The calm atmosphere and scenic beauty made us forget all our worries. We laughed, explored, 
        and made memories that will stay with us forever.
        It was more than just a trip—it was a reminder of how special time with friends can be.`
    },
    {
        title: "Hackathon 2024",
        author: "Sachin",
        date: "Oct 21, 2024",
        image: "photos/Hackathon.jpg",
        description: `Recently, our team had the opportunity to participate in the GP Purena Hackathon,
        a thrilling event filled with creativity, coding, and collaboration. 
        I teamed up with my three friends to take on the challenge.
        Together, we brainstormed ideas, divided tasks based on our strengths, 
        and worked tirelessly to bring our project to life.
        The hackathon was an intense yet exciting experience where we pushed our limits,
        learned new skills, and explored innovative solutions to real-world problems. 
        From late-night coding sessions to quick problem-solving under time pressure, 
        every moment tested our teamwork and determination.
        Although the competition was tough, the energy, enthusiasm, and support from everyone
        at the event made it unforgettable. This experience not only enhanced our technical skills
        but also strengthened our friendship and ability to work together as a team.`
    },
    {
        title: "Tour of Bhagalpur",
        author: "Sachin",
        date: "June 12, 2024",
        image: "photos/img_1.jpg",
        description: `Located at the Southern part of Bihar, it is one of the oldest districts of
        Bihar known for
        producing very good
        quality silk fabric and was once famous as 'Silk City'.`
    },
    {
        title: "Holi in Collage",
        author: "Sachin",
        date: "Mar 12, 2024",
        image: "photos/img_13.jpg",
        description: `Holi, Hindu spring festival celebrated in India and Nepal on the full-moon
        day of Phalguna
        (February - March). Participants throw colored water and colored powders on
        one another, and
        license is given to deviate from the usual societal
        norms and rankings of caste, gender, status, and age.`
    },
    {
        title: "V - Mart (Purnea)",
        author: "Sachin",
        date: "Dec 14, 2023",
        image: "photos/img_2.jpg",
        description: `V-Mart offers excellent products in clothing and accessories with amazing
        discounts. The
        quality of the products is top-notch and the variety is impressive. This
        makes it a one-stop
        destination for all your
        fashion needs. Don’t miss out on the great deals at V-Mart!`
    }
];

// Target container where blogs will be shown
const blogContainer = document.getElementById("blogsContainer");

// Render blogs dynamically
blogs.forEach(blog => {
    const blogEl = document.createElement("div");
    blogEl.classList.add("blogs-main");

    blogEl.innerHTML = `
        <div class="blogs-imgs">
            <img loading="lazy" class="img-blog" src="${blog.image}" alt="Image">
        </div>
        <div class="blog-content">
            <h2 class="blog-title">${blog.title}</h2>
            <div class="disc">Posted by ${blog.author} on <a href="#">${blog.date}</a></div>
            <p>${blog.description}</p>
        </div>
    `;
    blogContainer.appendChild(blogEl);
});
