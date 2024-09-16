var gasChart;
var gasPlot;
var gasSeries = {};
var socketGas1 = new WebSocket("ws://localhost:8080/ws/all-gas-data/" + cell_number);

// Подключение к WebSocket для данных по заменам газа
socketGas1.onopen = function() {
    console.log("WebSocket connection for gas changes established");
};

// Функция для обновления графика замен газа
function updateGasChart(data) {
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    for (var gasType in data) {
        if (Array.isArray(data[gasType])) {
            var processedData = sortDataByDate(processData(data[gasType]));

            if (!gasChart) {
                anychart.onDocumentReady(function() {
                    anychart.theme('darkGlamour');
                    gasChart = anychart.stock();
                    gasPlot = gasChart.plot(0);

                    gasPlot.xAxis().labels().format('dd-MM-yyyy');
                    gasPlot.xAxis().labels().padding(5);
                    gasPlot.yAxis().title('Количество замен');
                    gasPlot.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

                    gasSeries[gasType] = gasPlot.line(processedData).name(gasType);

                    gasChart.container('gas-schedule');
                    gasChart.draw();
                });
            } else {
                if (gasSeries[gasType]) {
                    gasSeries[gasType].data(processedData);
                } else {
                    gasSeries[gasType] = gasPlot.line(processedData).name(gasType);
                }
            }
        } else {
            console.error(`Data for gas type ${gasType} is not in expected format`);
        }
    }
}

// Обработка сообщения с сервера для замен газа
socketGas1.onmessage = function(event) {
    try {
        var data = JSON.parse(event.data);
        updateGasChart(data);
    } catch (error) {
        console.error('Error parsing data:', error);
    }
};