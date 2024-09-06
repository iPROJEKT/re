    anychart.onDocumentReady(function () {
      // create data set on our data
      var dataSet = anychart.data.set(getData());

      // map data for the first series, take x from the zero column and value from the first column of data set
      var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });

      // map data for the second series, take x from the zero column and value from the second column of data set
      var secondSeriesData = dataSet.mapAs({ x: 0, value: 2 });

      // map data for the third series, take x from the zero column and value from the third column of data set
      var thirdSeriesData = dataSet.mapAs({ x: 0, value: 3 });


      var fourSeriesData = dataSet.mapAs({ x: 0, value: 4 });

      // create line chart
      var chart = anychart.line();

      // turn on chart animation
      chart.animation(true);

      // set chart padding
      chart.padding([10, 20, 5, 20]);

      // turn on the crosshair
      chart.crosshair().enabled(true).yLabel(false).yStroke(null);

      // set tooltip mode to point
      chart.tooltip().positionMode('point');

      // set chart title text settings
      chart.title(
        'Расход газа'
      );

      // set yAxis title
      chart.yAxis().title('Литры');
      chart.xAxis().labels().padding(5);

      // create first series with mapped data
      var firstSeries = chart.line(firstSeriesData);
      firstSeries.name('Ar 100%');
      firstSeries.hovered().markers().enabled(true).type('circle').size(4);
      firstSeries
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(5);

      // create second series with mapped data
      var secondSeries = chart.line(secondSeriesData);
      secondSeries.name('Ar 98% CO2 2%');
      secondSeries.hovered().markers().enabled(true).type('circle').size(4);
      secondSeries
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(5);

      // create third series with mapped data
      var thirdSeries = chart.line(thirdSeriesData);
      thirdSeries.name('Ar 80% CO2 20%');
      thirdSeries.hovered().markers().enabled(true).type('circle').size(4);
      thirdSeries
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(5);

      var thirdSeries = chart.line(fourSeriesData);
      thirdSeries.name('He 100%');
      thirdSeries.hovered().markers().enabled(true).type('circle').size(4);
      thirdSeries
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(5);

      var thirdSeries = chart.line(thirdSeriesData);
      thirdSeries.name('CO2 100%');
      thirdSeries.hovered().markers().enabled(true).type('circle').size(4);
      thirdSeries
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(5);

      // turn the legend on
      chart.legend().enabled(true).fontSize(13).padding([0, 0, 10, 0]);

      // set container id for the chart
      chart.container('container');
      // initiate chart drawing
      chart.draw();
    });
