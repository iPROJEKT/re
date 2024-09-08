var tipChart;
var tipPlot;
var tipSeries = {};
var socketTip1 = new WebSocket("ws://localhost:8080/ws/all-tip-data/" + cell_number);

// Подключение к WebSocket для данных наконечников
socketTip1.onopen = function() {
    console.log("WebSocket connection for tip changes established");
};

// Функция для обновления графика замен наконечников
function updateTipChart(data) {
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    for (var diameter in data) {
        if (Array.isArray(data[diameter])) {
            var processedData = sortDataByDate(processData(data[diameter]));

            if (!tipChart) {
                anychart.onDocumentReady(function() {
                    anychart.theme('darkGlamour');
                    tipChart = anychart.stock();
                    tipPlot = tipChart.plot(0);

                    tipPlot.xAxis().labels().format('dd-MM-yyyy');
                    tipPlot.xAxis().labels().padding(5);
                    tipPlot.yAxis().title('Количество замен');
                    tipPlot.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

                    tipSeries[diameter] = tipPlot.line(processedData).name('Замены диаметра ' + diameter);

                    tipChart.container('tip-schedule');
                    tipChart.draw();
                });
            } else {
                if (tipSeries[diameter]) {
                    tipSeries[diameter].data(processedData);
                } else {
                    tipSeries[diameter] = tipPlot.line(processedData).name('Замены диаметра ' + diameter);
                }
            }
        } else {
            console.error(`Data for diameter ${diameter} is not in expected format`);
        }
    }
}

// Обработка сообщения с сервера для замен наконечников
socketTip1.onmessage = function(event) {
    try {
        var data = JSON.parse(event.data);
        updateTipChart(data);
    } catch (error) {
        console.error('Error parsing data:', error);
    }
};