var chart;
var plot;
var tipSeries;
var wareSeries;
var gazSeries;
var rollsSeries;
var intestineSeries;
var diffuserSeries;
var mudguardSeries;
var nozzleSeries;
var socket = new WebSocket("ws://localhost:8080/ws/tip-data/" + cell_number);

socket.onopen = function() {
    console.log("WebSocket connection established");
};

function formatDate(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}-${month}-${year}`;
}

// Функция для обновления графика
function updateChart(data) {

    // Функция для обработки данных и форматирования даты
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    // Обрабатываем и сортируем данные для каждой серии
    var processedTipData = sortDataByDate(processData(data.tip_data));
    var processedWareData = sortDataByDate(processData(data.ware_data));
    var processedGazData = sortDataByDate(processData(data.gaz_data));
    var processedRollsData = sortDataByDate(processData(data.rolls_data));
    var processedIntestineData = sortDataByDate(processData(data.intestine_data));
    var processedDiffuserData = sortDataByDate(processData(data.diffuser_data));
    var processedMudguardData = sortDataByDate(processData(data.mudguard_data));
    var processedNozzleData = sortDataByDate(processData(data.nozzle_data));

    if (!chart) {
        anychart.onDocumentReady(function() {
            anychart.theme('darkGlamour');
            chart = anychart.stock(); // Используем anychart.stock для создания графика
            plot = chart.plot(0);

            // Настраиваем оси и легенду
            plot.xAxis().labels().format('dd-MM-yyyy');
            plot.xAxis().labels().padding(5);
            plot.yAxis().title('Количество замен');

            plot.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

            // Создаем серии и добавляем их на график
            tipSeries = plot.line(processedTipData).name('Замены наконечников');
            wareSeries = plot.line(processedWareData).name('Замены проволоки');
            gazSeries = plot.line(processedGazData).name('Замены газа');
            rollsSeries = plot.line(processedRollsData).name('Замены роликов');
            intestineSeries = plot.line(processedIntestineData).name('Замены кишечника');
            diffuserSeries = plot.line(processedDiffuserData).name('Замены диффузора');
            mudguardSeries = plot.line(processedMudguardData).name('Замены брызговика');
            nozzleSeries = plot.line(processedNozzleData).name('Замены сопла');

            chart.container('container');
            chart.draw();
        });
    } else {
        // Обновляем данные существующих серий
        if (tipSeries) tipSeries.data(processedTipData);
        if (wareSeries) wareSeries.data(processedWareData);
        if (gazSeries) gazSeries.data(processedGazData);
        if (rollsSeries) rollsSeries.data(processedRollsData);
        if (intestineSeries) intestineSeries.data(processedIntestineData);
        if (diffuserSeries) diffuserSeries.data(processedDiffuserData);
        if (mudguardSeries) mudguardSeries.data(processedMudguardData);
        if (nozzleSeries) nozzleSeries.data(processedNozzleData);
    }
}

socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    updateChart(data);
};

socket.onerror = function(error) {
    console.error("WebSocket error:", error);
};

socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
    } else {
        console.error(`Connection died`);
    }
};