document.addEventListener("DOMContentLoaded", function () {
  // Toggle right sidebar (Filter panel)
  const toggleFilterBtn = document.getElementById("toggleFilter");
  const closeFilterBtn = document.getElementById("closeFilter");
  const rightSidebar = document.querySelector(".sidebar-right");

  if (toggleFilterBtn && rightSidebar) {
    toggleFilterBtn.addEventListener("click", () => {
      rightSidebar.classList.toggle("active");
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

  // Toggle left sidebar (☰ button)
  const toggleSidebarBtn = document.getElementById("toggleSidebar");
  const leftSidebar = document.getElementById("sidebar");

  if (toggleSidebarBtn && leftSidebar) {
    toggleSidebarBtn.addEventListener("click", () => {
      leftSidebar.classList.toggle("collapsed");
    });
  }

  // Toggle submenu under "My Info"
  const mainLinks = document.querySelectorAll(".main-link");

  mainLinks.forEach(link => {
    link.addEventListener("click", () => {
      const submenuId = link.dataset.parent + "-submenu";
      const submenu = document.getElementById(submenuId);

      if (submenu) {
        submenu.style.display = submenu.style.display === "none" ? "block" : "none";
      }
    });
  });
});

document.querySelectorAll('.tab-link').forEach(link => {
  link.addEventListener('click', () => {
    // Remove active class from all tab links
    document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
    link.classList.add('active');

    // Hide all tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

    // Show selected tab pane
    const targetId = link.dataset.tab;
    const targetPane = document.getElementById(targetId);
    if (targetPane) {
      targetPane.classList.add('active');
    }
  });
});

