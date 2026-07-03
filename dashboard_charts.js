document.addEventListener('DOMContentLoaded', () => {
    // Activity Chart (Applications over time)
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    new Chart(activityCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Applications',
                data: [2, 5, 3, 8, 4, 1, 6],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: { display: false },
                x: { grid: { display: false } }
            }
        }
    });

    // Skills Radar Chart
    const skillCtx = document.getElementById('skillRadar').getContext('2d');
    new Chart(skillCtx, {
        type: 'radar',
        data: {
            labels: ['Python', 'Django', 'UI Design', 'Backend', 'Database', 'Soft Skills'],
            datasets: [{
                label: 'Your Mastery',
                data: [90, 85, 60, 80, 75, 70],
                backgroundColor: 'rgba(168, 85, 247, 0.2)',
                borderColor: '#a855f7',
                pointBackgroundColor: '#a855f7'
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                r: {
                    angleLines: { display: false },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            }
        }
    });
});
