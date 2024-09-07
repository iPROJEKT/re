var socket = new WebSocket("ws://localhost:8080/ws/robot-state/" + cell_number);

socket.onopen = function() {
    console.log("WebSocket connection established");
};
socket.onmessage = function(event) {
    var data = JSON.parse(event.data);
    console.log('Data received:', data);
    document.getElementById('wire').textContent = data.wire || '-';
    document.getElementById('wire_time').textContent = data.wire_time || '-';

    document.getElementById('main_gaz').textContent = data.main_gaz || '-';
    document.getElementById('main_gaz_time').textContent = data.main_gaz_time || '-';

    document.getElementById('add_gaz').textContent = data.add_gaz || '-';
    document.getElementById('add_gaz_time').textContent = data.add_gaz_time || '-';

    document.getElementById('tip').textContent = data.tip || '-';
    document.getElementById('tip_type').textContent = data.tip_type || '-';
    document.getElementById('tip_time').textContent = data.tip_time || '-';

    document.getElementById('roll').textContent = data.roll || '-';
    document.getElementById('roll_type').textContent = data.roll_type || '-';
    document.getElementById('roll_dim').textContent = data.roll_dim || '-';

    document.getElementById('mudguard').textContent = data.mudguard || '-';
    document.getElementById('mudguard_time').textContent = data.mudguard_time || '-';

    document.getElementById('thread').textContent = data.thread || '-';
    document.getElementById('thread_time').textContent = data.thread_time || '-';

    document.getElementById('nozzle').textContent = data.nozzle || '-';
        document.getElementById('nozzle_time').textContent = data.nozzle_time || '-';
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