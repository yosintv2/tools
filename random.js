const currentPage = location.pathname.split("/").pop();

    const pages = [
      { title: "Lok Sewa Nepal", link: "/loksewa-nepal/" },
      { title: "General Knowledge", link: "/general-knowledge/" },
      { title: "Sports", link: "/sports/" },
      { title: "Current Affairs", link: "/current-affairs/" },
      { title: "History", link: "/history/" },
      { title: "Math Quiz", link: "/math/" },
      { title: "Science Quiz", link: "/science/" },
      { title: "Programming", link: "/programming/" },
      { title: "Pop Culture", link: "/pop-culture/" },
      { title: "Languages", link: "/languages/" },
      { title: "Custom Quiz", link: "/custom/" }
    ];

    const otherPages = pages.filter(p => !currentPage.includes(p.link));

    const randomPages = otherPages
      .sort(() => 0.5 - Math.random())
      .slice(0, 9);

    const container = document.getElementById("random-pages-container");

    container.innerHTML = randomPages.map(p => `
      <div class="col-md-4 mb-3">
        <a href="${p.link}" class="btn btn-primary w-100">${p.title}</a>
      </div>
    `).join('');
