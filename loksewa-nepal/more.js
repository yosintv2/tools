const currentPage = location.pathname.split("/").pop();
const pages = [
  { title: "Lok Sewa Set 1 Quiz", link: "set1.html" },
  { title: "Lok Sewa Set 2 Quiz", link: "set2.html" },
  { title: "Lok Sewa Set 3 Quiz", link: "set3.html" },
  { title: "Lok Sewa Set 4 Quiz", link: "set4.html" },
  { title: "Lok Sewa Set 5 Quiz", link: "/loksewa-nepal/set5.html" },
  { title: "Lok Sewa Set 6 Quiz", link: "/loksewa-nepal/set6.html" },
  { title: "Lok Sewa Set 7 Quiz", link: "/loksewa-nepal/set7.html" },
  { title: "Lok Sewa Set 8 Quiz", link: "/loksewa-nepal/set8.html" },
  { title: "Lok Sewa Set 9 Quiz", link: "/loksewa-nepal/set9.html" },
  { title: "Lok Sewa Set 10 Quiz", link: "/loksewa-nepal/set10.html" },
  { title: "Lok Sewa Set 11 Quiz", link: "/loksewa-nepal/set11.html" }
    ];

    const otherPages = pages.filter(p => !currentPage.includes(p.link));

    const randomPages = otherPages
      .sort(() => 0.5 - Math.random())
      .slice(0, 3);

    const container = document.getElementById("more-container");

    container.innerHTML = randomPages.map(p => `
      <div class="col-md-4 mb-3">
        <a href="${p.link}" class="btn btn-primary w-100">${p.title}</a>
      </div>
    `).join('');
