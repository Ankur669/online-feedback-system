// Form validation
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(event) {
            const message = document.querySelector("textarea").value.trim();
            if (message.length < 5) {
                alert("Feedback must be at least 5 characters long!");
                event.preventDefault();
            }
        });
    }
});

// Dark mode toggle
document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = "🌙 Toggle Dark Mode";
    toggleBtn.style.margin = "10px auto";
    toggleBtn.style.display = "block";
    document.body.insertBefore(toggleBtn, document.body.firstChild);

    toggleBtn.addEventListener("click", function() {
        document.body.classList.toggle("dark");
    });
});

// Chart.js sentiment visualization
document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById("sentimentChart");
    if (ctx && typeof sentimentData !== "undefined") {
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: sentimentData,
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
});
