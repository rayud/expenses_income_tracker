const renderIncomeChart = (labels, data, backgroundColor, borderColor) => {
    const ctx = document.getElementById('myChart1');
    ctx.width = 500;
    ctx.height = 500;
    var chart_instance1 = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            // labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'Last 6 months data',
                data: data,
                //   data: [12, 19, 3, 5, 2, 3],
                backgroundColor: backgroundColor,
                borderColor: borderColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Category Expense Summary in Doughnut chart'
                }
            }
        }
    });


    const ctx1 = document.getElementById('SecondChart1');
    ctx1.width = 500;
    ctx1.height = 500;
    var chart_instance2 = new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: labels,
            // labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'Last 6 months data',
                data: data,
                //   data: [12, 19, 3, 5, 2, 3],
                borderColor: borderColor,
                backgroundColor: backgroundColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Category Expense Summary in Bar Chart'
                }
            }
        }
    });



}
const getIncomeChartData = () => {
    fetch("/income/income_category_summary/", )
        .then((res) => res.json())
        .then((result) => {
            backgroundColor = [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ];
            borderColor = [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ];
            renderIncomeChart(Object.keys(result.income_category_summary), Object.values(result.income_category_summary), backgroundColor, borderColor);
        });
}

document.addEventListener('onloads', getIncomeChartData());