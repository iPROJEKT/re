var defectChart;
var defectPlot;
var defectSeries = {};
var socketDefects = new WebSocket("ws://localhost:8080/ws/all-defect-data/" + cell_number);

// Подключение к WebSocket для данных по дефектам
socketDefects.onopen = function() {
    console.log("WebSocket connection for defect data established");
};

// Функция для обновления графика дефектов
function updateDefectChart(data) {
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);  // Комментарий исключен, оставлены только дата и количество
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    for (var defectName in data) {
        if (Array.isArray(data[defectName])) {
            var processedData = sortDataByDate(processData(data[defectName]));

            if (!defectChart) {
                anychart.onDocumentReady(function() {
                    anychart.theme('darkGlamour');
                    defectChart = anychart.stock();
                    defectPlot = defectChart.plot(0);

                    defectPlot.xAxis().labels().format('dd-MM-yyyy');
                    defectPlot.xAxis().labels().padding(5);
                    defectPlot.yAxis().title('Количество дефектов');
                    defectPlot.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

                    defectSeries[defectName] = defectPlot.line(processedData).name(defectName);

                    defectChart.container('defect-schedule');
                    defectChart.draw();
                });
            } else {
                if (defectSeries[defectName]) {
                    defectSeries[defectName].data(processedData);
                } else {
                    defectSeries[defectName] = defectPlot.line(processedData).name(defectName);
                }
            }
        } else {
            console.error(`Data for defect ${defectName} is not in expected format`);
        }
    }
}

// Обработка сообщения с сервера для дефектов
socketDefects.onmessage = function(event) {
    try {
        var data = JSON.parse(event.data);
        updateDefectChart(data);
    } catch (error) {
        console.error('Error parsing data:', error);
    }
};