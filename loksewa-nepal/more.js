// List of all pages with their categories
const pages = [
  { title: "Lok Sewa Nepal", link: "/loksewa-nepal/", category: "Government" },
  { title: "General Knowledge", link: "/general-knowledge/", category: "Knowledge" },
  { title: "Sports", link: "/sports/", category: "Sports" },
  { title: "Current Affairs", link: "/current-affairs/", category: "Knowledge" },
  { title: "History", link: "/history/", category: "Knowledge" },
  { title: "Math Quiz", link: "/math/", category: "Education" },
  { title: "Science Quiz", link: "/science/", category: "Education" },
  { title: "Programming", link: "/programming/", category: "Tech" },
  { title: "Pop Culture", link: "/pop-culture/", category: "Culture" },
  { title: "Languages", link: "/languages/", category: "Education" },
  { title: "Custom Quiz", link: "/custom/", category: "Quiz" }
];

// Get the current page's category from the URL
const currentPage = location.pathname.split("/").pop();
const currentPageCategory = pages.find(p => p.link === `/${currentPage}`)?.category;

// Function to render Random Pages
function renderRandomPages() {
  const otherPages = pages.filter(p => !currentPage.includes(p.link));

  const randomPages = otherPages
    .sort(() => 0.5 - Math.random())
    .slice(0, 3);

  const container = document.getElementById("random-pages-container");
  if (container) {
    container.innerHTML = randomPages.map(p => `
      <div class="col-md-4 mb-3">
        <a href="${p.link}" class="btn btn-primary w-100">${p.title}</a>
      </div>
    `).join('');
  }
}

// Function to render Related Pages
function renderRelatedPages() {
  const relatedPages = pages.filter(p => p.category === currentPageCategory && p.link !== `/${currentPage}`);

  const container = document.getElementById("related-pages-container");
  if (container) {
    container.innerHTML = relatedPages.map(p => `
      <div class="col-md-4 mb-3">
        <a href="${p.link}" class="btn btn-secondary w-100">${p.title}</a>
      </div>
    `).join('');
  }
}

// Call the functions to render pages on load
renderRandomPages();
renderRelatedPages();
