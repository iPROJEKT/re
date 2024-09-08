var chart1;
var plot1;
var tipSeries;
var wareSeries;
var gazSeries;
var rollsSeries;
var intestineSeries;
var diffuserSeries;
var mudguardSeries;
var nozzleSeries;
var socket1 = new WebSocket("ws://localhost:8080/ws/all-data/" + cell_number);

socket1.onopen = function() {
    console.log("WebSocket connection 1 established");
};

// Функция для обновления первого графика
function updateChart1(data) {
    // Обрабатываем и сортируем данные для каждой серии
    function processData(data) {
        return data.map(item => [new Date(item[0]).getTime(), item[1]]);
    }

    function sortDataByDate(data) {
        return data.sort((a, b) => a[0] - b[0]);
    }

    var processedTipData = sortDataByDate(processData(data.tip_data));
    var processedWareData = sortDataByDate(processData(data.ware_data));
    var processedGazData = sortDataByDate(processData(data.gaz_data));
    var processedRollsData = sortDataByDate(processData(data.rolls_data));
    var processedIntestineData = sortDataByDate(processData(data.intestine_data));
    var processedDiffuserData = sortDataByDate(processData(data.diffuser_data));
    var processedMudguardData = sortDataByDate(processData(data.mudguard_data));
    var processedNozzleData = sortDataByDate(processData(data.nozzle_data));

    if (!chart1) {
        anychart.onDocumentReady(function() {
            anychart.theme('darkGlamour');
            chart1 = anychart.stock();
            plot1 = chart1.plot(0);

            plot1.xAxis().labels().format('dd-MM-yyyy');
            plot1.xAxis().labels().padding(5);
            plot1.yAxis().title('Количество замен');
            plot1.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

            tipSeries = plot1.line(processedTipData).name('Замены наконечников');
            wareSeries = plot1.line(processedWareData).name('Замены проволоки');
            gazSeries = plot1.line(processedGazData).name('Замены газа');
            rollsSeries = plot1.line(processedRollsData).name('Замены роликов');
            intestineSeries = plot1.line(processedIntestineData).name('Замены кишечника');
            diffuserSeries = plot1.line(processedDiffuserData).name('Замены диффузора');
            mudguardSeries = plot1.line(processedMudguardData).name('Замены брызговика');
            nozzleSeries = plot1.line(processedNozzleData).name('Замены сопла');

            chart1.container('container');
            chart1.draw();
        });
    } else {
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

socket1.onmessage = function(event) {
    var data = JSON.parse(event.data);
    updateChart1(data);
};