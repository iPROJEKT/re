anychart.onDocumentReady(function () {
      anychart.theme('darkEarth');
      var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });

      // map data for the second series, take x from the zero column and value from the second column of data set
      var secondSeriesData = dataSet.mapAs({ x: 0, value: 2 });

      // create column chart
      var chart = anychart.column();

      // turn on chart animation
      chart.animation(true);

      // set chart title text settings
      chart.title('Замены / Израсходванно за 2 дня');

      // temp variable to store series instance
      var series;

      var setupSeries = function (series, name) {
        series.name(name);
        series.selected().fill('#f48fb1 1.5').stroke('1.5 #c2185b');
      };

      // create first series with mapped data
      series = chart.column(firstSeriesData);
      series.xPointPosition(0.45);
      setupSeries(series, 'Замены');

      // create second series with mapped data
      series = chart.column(secondSeriesData);
      series.xPointPosition(0.25);
      setupSeries(series, 'Кг материала');

      // set chart padding
      chart.barGroupsPadding(0.3);

      // format numbers in y axis label to match browser locale
      chart.yAxis().labels().format('{%Value}{groupsSeparator: }');

      // set titles for Y-axis
      chart.yAxis().title('Кол-во');

      // turn on legend
      chart.legend().enabled(true).fontSize(13).padding([0, 0, 20, 0]);

      chart.interactivity().hoverMode('single');

      chart.tooltip().format('{%Value}{groupsSeparator: }');

      // set container id for the chart
      chart.container('graf');

      // initiate chart drawing
      chart.draw();
});