var wireChart;
var wirePlot;
var wireSeries = {};
var socketWire1 = new WebSocket("ws://localhost:8080/ws/all-wire-data/" + cell_number);

// Подключение к WebSocket для данных проволок
socketWire1.onopen = function() {
    console.log("WebSocket connection for wire changes established");
};

// Инициализация графика замен проволок
anychart.onDocumentReady(function() {
    anychart.theme('darkGlamour');
    wireChart = anychart.stock();
    wirePlot = wireChart.plot(0);

    wirePlot.xAxis().labels().format('dd-MM-yyyy');
    wirePlot.xAxis().labels().padding(5);
    wirePlot.yAxis().title('Количество замен');
    wirePlot.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

    wireChart.container('wire-schedule');
    wireChart.draw();
});

// Функция для обновления данных графика замен проволок
function updateWireChart(data) {
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    // Проход по сортам проволоки и обновление данных
    for (var brand in data) {
        var processedData = sortDataByDate(processData(data[brand]));

        if (!wireSeries[brand]) {
            // Если серия для данного сорта проволоки ещё не создана, создаём новую серию
            wireSeries[brand] = wirePlot.line(processedData).name('Замены ' + brand);
        } else {
            // Если серия уже существует, обновляем её данные
            wireSeries[brand].data(processedData);
        }
    }
}

// Обработка сообщения с сервера для замен проволок
socketWire1.onmessage = function(event) {
    var data = JSON.parse(event.data);
    updateWireChart(data);
};