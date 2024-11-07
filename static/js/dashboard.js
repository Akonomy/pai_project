

//SCRIPTS   

function sendPresetValue(sensorId, value) {
    document.getElementById(`value-display-${sensorId}`).innerText = value; // Update display with preset value
    document.querySelector(`#sensor-${sensorId} .range-slider`).value = value; // Update slider to reflect preset value

    // Send the preset value as an analog command
    fetch(sendCommandUrl, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json", 
            "X-CSRFToken": csrfToken 
        },
        body: JSON.stringify({ sensor_id: sensorId, command: "set_value", value: value })
    })
    .then(response => response.json())
    .then(data => console.log(data.message || "Preset value updated successfully"));
}

function sendDigitalCommand(sensorId, status) {
    fetch(sendCommandUrl, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json", 
            "X-CSRFToken": csrfToken 
        },
        body: JSON.stringify({ sensor_id: sensorId, command: status })
    })
    .then(response => response.json())
    .then(data => console.log(data.message || "Command sent successfully"));
}

function sendAnalogValue(sensorId, value) {
    document.getElementById(`value-display-${sensorId}`).innerText = value;
    fetch(sendCommandUrl, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json", 
            "X-CSRFToken": csrfToken 
        },
        body: JSON.stringify({ sensor_id: sensorId, command: "set_value", value: value })
    })
    .then(response => response.json())
    .then(data => console.log(data.message || "Value updated successfully"));
}

let previousSensorData = {};


function fetchSensorData() {
    fetch(sensorDataUrl)
        .then(response => response.json())
        .then(data => {
            updateDivsIfDataChanged(data);
            previousSensorData = data;
        })
        .catch(error => console.error('Error fetching sensor data:', error));
}

function updateDivsIfDataChanged(newData) {
    let isChanged = false;

    for (let sensorId in newData) {
        const sensorData = newData[sensorId];
        const previousData = previousSensorData[sensorId];

        if (!previousData || JSON.stringify(sensorData) !== JSON.stringify(previousData)) {
            isChanged = true;
        }
    }

    if (isChanged) {
        for (let sensorId in newData) {
            updateSensorDiv(sensorId, newData[sensorId]);
        }
    }
}

function updateSensorDiv(sensorId, sensorData) {
    const sensorDiv = document.getElementById(`sensor-${sensorId}`);
    if (sensorDiv) {
        const statusElement = sensorDiv.querySelector(".sensor-status");
        if (statusElement) {
            statusElement.textContent = sensorData.status;
        }

        const valueElement = sensorDiv.querySelector(".sensor-value");
        if (valueElement) {
            valueElement.textContent = sensorData.value;
        }

        sensorDiv.classList.remove("bg-blue", "bg-orange");


      // Set background color based on sensor ID
        if (sensorData.status == "high" && sensorId === "sensor_1") {
            sensorDiv.classList.add("bg-blue");
        }
        if (sensorData.status == "high" && sensorId === "sensor_2") {
            sensorDiv.classList.add("bg-orange");
        }

        // Set background color based on sensor ID
        if (sensorData.value == 1 && sensorId === "sensor_9") {
            sensorDiv.classList.add("bg-blue");
        }
        if (sensorData.value == 1 && sensorId === "sensor_8") {
            sensorDiv.classList.add("bg-orange");
        }

        const alpha = sensorData.value / 255;
        sensorDiv.style.backgroundColor = "";

        if (sensorId === "sensor_3") {
            sensorDiv.style.backgroundColor = `rgba(0, 255, 0, ${alpha})`;
        } else if (sensorId === "sensor_4") {
            sensorDiv.style.backgroundColor = `rgba(255, 0, 0, ${alpha})`;
        }
    }
}







setInterval(fetchSensorData, 1800);