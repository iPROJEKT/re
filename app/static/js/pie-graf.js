document.addEventListener('DOMContentLoaded', function() {
    // Функция для создания круговой диаграммы
    function createPieChart(containerId, title, data) {
        var chart = anychart.pie();
        chart.title(title);
        chart.data(data);
        chart.container(containerId);
        chart.draw();
    }

    // Функция для создания контейнера для диаграммы
    function createChartContainer(id) {
        const container = document.createElement('div');
        container.id = id;
        container.className = "pie-chart-container";
        document.getElementById('dia-container').appendChild(container);
        return container.id;
    }

    // Функция для отправки запроса на сервер с выбранным типом компонента
    function requestComponentData(type) {
        const request = {
            type: type
        };
        ws.send(JSON.stringify(request));
    }

    // Функция для обновления диаграмм
    function updateCharts(data) {
    console.log("Updating charts with data:", data); // Отладка

    // Очищаем контейнер перед добавлением новых диаграмм
    const diaContainer = document.getElementById('dia-container');
    diaContainer.innerHTML = "";

    // Получаем выбранный тип компонента
    const selectedType = document.getElementById('component-type').value;
    console.log("Selected component type:", selectedType); // Отладка

    // Обновляем графики в зависимости от данных
    if (selectedType === 'проволока') {
        if (data.wire_data && data.wire_data.length > 0) {
            data.wire_data.forEach(item => {
                console.log(`Creating wire chart for ${item.name}-${item.sub}`); // Отладка
                const containerId = createChartContainer(`wire-${item.name}-${item.sub}`);
                const chartData = [
                    ["Осталось", item.count],
                    ["Было", item.start_count]
                ];
                createPieChart(containerId, `Проволока: ${item.name} ${item.sub}`, chartData);
            });
        } else {
            console.log("No data available for проволока");
        }
    } else if (selectedType === 'наконечник') {
        if (data.tip_data && data.tip_data.length > 0) {
            data.tip_data.forEach(item => {
                console.log(`Creating tip chart for ${item.name}-${item.sub}`); // Отладка
                const containerId = createChartContainer(`tip-${item.name}-${item.sub}`);
                const chartData = [
                    ["Осталось", item.count],
                    ["Было", item.start_count]
                ];
                createPieChart(containerId, `Наконечник: ${item.name} ${item.sub}`, chartData);
            });
        } else {
            console.log("No data available for наконечник");
        }
    } else if (selectedType === 'газ') {
        if (data.gas_data && data.gas_data.length > 0) {
            data.gas_data.forEach(item => {
                console.log(`Creating gas chart for ${item.name}-${item.sub}`); // Отладка
                const containerId = createChartContainer(`gas-${item.name}-${item.sub}`);
                const chartData = [
                    ["Осталось", item.count],
                    ["Было", item.start_count]
                ];
                createPieChart(containerId, `Газ: ${item.name} ${item.sub}`, chartData);
            });
        } else {
            console.log("No data available for газ");
        }
    } else {
        console.log(`Unknown component type: ${selectedType}`);
    }
}

    // Подключение к WebSocket
    const ws = new WebSocket('ws://localhost:8080/ws/material/control/');

    ws.onopen = function() {
        console.log("WebSocket connection opened"); // Отладка
        // Изначально отправляем запрос на проволоку
        requestComponentData('проволока');
    };

    ws.onmessage = function(event) {
        console.log("WebSocket message received:", event.data); // Отладка
        const response = JSON.parse(event.data);
        updateCharts(response);
    };

    ws.onerror = function(event) {
        console.error("WebSocket error observed:", event);
    };

    ws.onclose = function() {
        console.log("WebSocket connection closed"); // Отладка
    };

    // Обработчик изменения выбора типа компонента
    document.getElementById('component-type').addEventListener('change', function(event) {
        const selectedType = event.target.value;
        console.log("Component type selected:", selectedType); // Отладка
        requestComponentData(selectedType);
    });
});