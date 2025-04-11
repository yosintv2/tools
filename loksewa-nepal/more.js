// List of all pages with their categories
const pages = [
  { title: "Set 1 Quiz", link: "/loksewa-nepal/set1.html" },
  { title: "Set 2 Quiz", link: "/loksewa-nepal/set2.html" },
  { title: "Set 3 Quiz", link: "/loksewa-nepal/set3.html" },
  { title: "Set 4 Quiz", link: "/loksewa-nepal/set4.html" },
  { title: "Set 5 Quiz", link: "/loksewa-nepal/set5.html" },
  { title: "Set 6 Quiz", link: "/loksewa-nepal/set6.html" },
  { title: "Set 7 Quiz", link: "/loksewa-nepal/set7.html" },
  { title: "Set 8 Quiz", link: "/loksewa-nepal/set8.html" },
  { title: "Set 9 Quiz", link: "/loksewa-nepal/set9.html" },
  { title: "Set 10 Quiz", link: "/loksewa-nepal/set10.html" },
  { title: "Set 11 Quiz", link: "/loksewa-nepal/set11.html" },
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

  const container = document.getElementById("more-container");
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

  const container = document.getElementById("more-container");
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
