console.log("dashboard.js loaded ✅");

document.addEventListener("DOMContentLoaded", function () {
  const rightSidebar = document.querySelector(".sidebar-right");
  const filterTargetInput = document.getElementById("filterTarget");

  const toggleFilterWallets = document.getElementById("toggleFilterWallets");
  const toggleFilterRequests = document.getElementById("toggleFilterRequests");
  const closeFilterBtn = document.getElementById("closeFilter");

  const toggleFilterBtn = document.getElementById("toggleFilter");

  if (toggleFilterBtn && rightSidebar) {
    toggleFilterBtn.addEventListener("click", () => {
      rightSidebar.classList.add("active");
    });
  }

  if (toggleFilterWallets && rightSidebar && filterTargetInput) {
    toggleFilterWallets.addEventListener("click", function () {
      filterTargetInput.value = "wallets";
      rightSidebar.classList.add("active");
    });
  }

  if (toggleFilterRequests && rightSidebar && filterTargetInput) {
    toggleFilterRequests.addEventListener("click", () => {
      filterTargetInput.value = "requests";
      rightSidebar.classList.add("active");
    });
  }

  if (closeFilterBtn && rightSidebar) {
    closeFilterBtn.addEventListener("click", () => {
      rightSidebar.classList.remove("active");
    });
  }

  // Adjust right sidebar position based on header height
  const header = document.querySelector(".site-header");
  if (header && rightSidebar) {
    const headerHeight = header.offsetHeight;
    rightSidebar.style.top = headerHeight + "px";
    rightSidebar.style.height = `calc(100vh - ${headerHeight}px)`;
  }

  // Left sidebar toggle
  const toggleSidebarBtn = document.getElementById("toggleSidebar");
  const leftSidebar = document.getElementById("sidebar");

  if (toggleSidebarBtn && leftSidebar) {
    toggleSidebarBtn.addEventListener("click", () => {
      leftSidebar.classList.toggle("collapsed");
    });
  }

  // Submenu toggle
  document.querySelectorAll(".main-link").forEach(link => {
    link.addEventListener("click", () => {
      const submenuId = link.dataset.parent + "-submenu";
      const submenu = document.getElementById(submenuId);
      if (submenu) {
        submenu.style.display = submenu.style.display === "none" ? "block" : "none";
      }
    });
  });

  // Tab switching
  document.querySelectorAll(".submenu").forEach(submenu => {
    submenu.addEventListener("click", function (e) {
      const tabItem = e.target.closest(".tab-link");
      if (!tabItem || !tabItem.dataset.tab) return;

      document.querySelectorAll(".tab-link").forEach(l => l.classList.remove("active"));
      tabItem.classList.add("active");

      document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
      const targetPane = document.getElementById(tabItem.dataset.tab);
      if (targetPane) {
        targetPane.classList.add("active");
      }

      e.preventDefault();
    });
  });
});
