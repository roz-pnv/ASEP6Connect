document.addEventListener('DOMContentLoaded', function () {
  if (!window.motionChartData || !Array.isArray(window.motionChartData)) return;

  window.motionChartData.forEach(motion => {
    const canvas = document.getElementById(`voteChart${motion.id}`);
    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
      type: "pie",
      data: {
        labels: ["Yes", "No", "Abstain"],
        datasets: [{
          data: [motion.vote_yes, motion.vote_no, motion.vote_abstain],
          backgroundColor: ["#702386ff", "#bd1659ff", "#9c69dfff" ],
          borderColor: "#fff",
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              font: { size: 14 },
              color: "#333"
            }
          },
          title: {
            display: true,
            text: `Vote Distribution for Motion ${motion.id}`,
            font: {
              size: 16,
              weight: "bold"
            },
            color: "#444"
          }
        }
      }
    });
  });
});
