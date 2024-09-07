const ws = new WebSocket('ws://localhost:8080/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    const time = data.time;
    const robot_1 = data.robots["1"];
    const robot_2 = data.robots["2"];

    // Обновляем время
    document.getElementById('current-time-left').textContent = time;
    document.getElementById('current-time-right').textContent = time;

    // Обновляем данные для Установки 1
    document.getElementById('current-wire-mark-left').textContent = robot_1.wire;
    document.getElementById('current-wire-diameter-left').textContent = robot_1.wire_diameter;

    // Обновляем данные для Установки 2
    document.getElementById('current-wire-mark-right').textContent = robot_2.wire;
    document.getElementById('current-wire-diameter-right').textContent = robot_2.wire_diameter;
};

ws.onopen = function() {
    console.log('WebSocket connection opened');
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
};

ws.onerror = function(error) {
    console.log('WebSocket error: ', error);
};