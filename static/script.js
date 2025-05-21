function checkCorrelation() {
    const ticker1 = document.getElementById("ticker1").value;
    const ticker2 = document.getElementById("ticker2").value;

    const resultEl = document.getElementById("result");
    const loadingEl = document.getElementById("loading");

    resultEl.innerText = "";
    loadingEl.style.display = "block"; // показать "загрузка"

    fetch(`/correlate?ticker1=${ticker1}&ticker2=${ticker2}`)
        .then(response => response.json())
        .then(data => {
            loadingEl.style.display = "none"; // скрыть "загрузка"
            if (data.correlation !== undefined) {
                resultEl.innerText = `Корреляция: ${data.correlation}`;
            } else {
                resultEl.innerText = `Ошибка: ${data.error}`;
            }
            drawChart(ticker1, ticker2);
        })
        .catch(error => {
            loadingEl.style.display = "none"; // скрыть "загрузка"
            resultEl.innerText = `Ошибка: ${error}`;
        });
}

function drawChart(ticker1, ticker2) {
    fetch(`/prices?ticker1=${ticker1}&ticker2=${ticker2}`)
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('priceChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: ticker1,
                            data: data.series1,
                            borderColor: 'blue',
                            fill: false
                        },
                        {
                            label: ticker2,
                            data: data.series2,
                            borderColor: 'green',
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'top' },
                        title: { display: true, text: 'Динамика цен' }
                    }
                }
            });
        });
}
