const currentPage = location.pathname.split("/").pop();
const pages = [
  { title: "Set 1 Quiz", link: "set1.html" },
  { title: "Set 2 Quiz", link: "set2.html" },
  { title: "Set 3 Quiz", link: "set3.html" },
  { title: "Set 4 Quiz", link: "set4.html" },
  { title: "Set 5 Quiz", link: "/loksewa-nepal/set5.html" },
  { title: "Set 6 Quiz", link: "/loksewa-nepal/set6.html" },
  { title: "Set 7 Quiz", link: "/loksewa-nepal/set7.html" },
  { title: "Set 8 Quiz", link: "/loksewa-nepal/set8.html" },
  { title: "Set 9 Quiz", link: "/loksewa-nepal/set9.html" },
  { title: "Set 10 Quiz", link: "/loksewa-nepal/set10.html" },
  { title: "Set 11 Quiz", link: "/loksewa-nepal/set11.html" }
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
