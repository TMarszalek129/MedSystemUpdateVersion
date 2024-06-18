function renderChart(canvasId, labels, data, label, borderColor,unit) {
    const ctx = document.getElementById(canvasId);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: borderColor,
                borderWidth: 1,
                fill: false
            }]
        },

        options: {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: unit
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Timestamp'
                    }
                }
            }
        }


    });

}

