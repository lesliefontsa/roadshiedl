// SomnoControl JavaScript Functions

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeSpeedChart();
    startRealTimeUpdates();
    setupEventListeners();
});

// Speed Chart Configuration
function initializeSpeedChart() {
    const ctx = document.getElementById('speedChart').getContext('2d');
    
    window.speedChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'TRK-001 (Jean)',
                data: [],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.1
            }, {
                label: 'TRK-002 (Marie)',
                data: [],
                borderColor: '#ffc107',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                tension: 0.1
            }, {
                label: 'TRK-003 (Pierre)',
                data: [],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Vitesses en Temps Réel (km/h)'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 120,
                    ticks: {
                        callback: function(value) {
                            return value + ' km/h';
                        }
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Temps'
                    }
                }
            },
            elements: {
                point: {
                    radius: 3,
                    hoverRadius: 6
                }
            }
        }
    });
    
    // Add initial data
    updateSpeedChart();
}

// Update Speed Chart with new data
function updateSpeedChart() {
    const now = new Date();
    const timeLabel = now.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit' 
    });
    
    // Simulate real-time speed data
    const speeds = {
        trk001: Math.floor(Math.random() * 20) + 65, // 65-85 km/h
        trk002: Math.floor(Math.random() * 25) + 85, // 85-110 km/h
        trk003: Math.floor(Math.random() * 30) + 90  // 90-120 km/h
    };
    
    // Update chart data
    if (window.speedChart.data.labels.length > 20) {
        window.speedChart.data.labels.shift();
        window.speedChart.data.datasets.forEach(dataset => {
            dataset.data.shift();
        });
    }
    
    window.speedChart.data.labels.push(timeLabel);
    window.speedChart.data.datasets[0].data.push(speeds.trk001);
    window.speedChart.data.datasets[1].data.push(speeds.trk002);
    window.speedChart.data.datasets[2].data.push(speeds.trk003);
    
    window.speedChart.update('none');
}

// Real-time updates simulation
function startRealTimeUpdates() {
    // Update chart every 5 seconds
    setInterval(updateSpeedChart, 5000);
    
    // Update vehicle monitoring table every 3 seconds
    setInterval(updateVehicleMonitoring, 3000);
    
    // Check for critical alerts every 10 seconds
    setInterval(checkCriticalAlerts, 10000);
}

// Update vehicle monitoring table
function updateVehicleMonitoring() {
    const tableBody = document.getElementById('vehicleMonitoring');
    const rows = tableBody.querySelectorAll('tr');
    
    rows.forEach((row, index) => {
        const speedCell = row.querySelector('td:nth-child(4) .fw-bold');
        const timeCell = row.querySelector('td:nth-child(6)');
        
        if (speedCell && timeCell) {
            // Update timestamp
            const randomSeconds = Math.floor(Math.random() * 60) + 10;
            timeCell.textContent = `Il y a ${randomSeconds} sec`;
            
            // Update speed with some variation
            let currentSpeed = parseInt(speedCell.textContent);
            let newSpeed = currentSpeed + (Math.random() * 10 - 5); // ±5 km/h variation
            newSpeed = Math.max(50, Math.min(120, Math.round(newSpeed))); // Keep within 50-120 range
            
            speedCell.textContent = `${newSpeed} km/h`;
            
            // Update speed limit warning color
            const limitElement = speedCell.nextElementSibling.querySelector('small');
            if (newSpeed > 90) {
                limitElement.className = 'text-danger';
                speedCell.className = 'fw-bold text-danger';
            } else if (newSpeed > 85) {
                limitElement.className = 'text-warning';
                speedCell.className = 'fw-bold text-warning';
            } else {
                limitElement.className = 'text-success';
                speedCell.className = 'fw-bold';
            }
        }
    });
}

// Check for critical alerts
function checkCriticalAlerts() {
    // Simulate random critical alert (10% chance)
    if (Math.random() < 0.1) {
        showEmergencyModal();
    }
}

// Show emergency modal
function showEmergencyModal() {
    const modal = new bootstrap.Modal(document.getElementById('emergencyModal'));
    modal.show();
    
    // Play alert sound (if available)
    playAlertSound();
}

// Play alert sound
function playAlertSound() {
    // Create audio context for alert sound
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        
        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.5);
    } catch (error) {
        console.log('Audio not supported');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Navigation active state
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Filter buttons
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.btn-group .btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterVehicles(this.textContent.trim());
        });
    });
    
    // Quick action buttons
    document.querySelector('.btn-danger').addEventListener('click', function() {
        if (confirm('Êtes-vous sûr de vouloir déclencher un arrêt d\'urgence global ?')) {
            alert('Arrêt d\'urgence déclenché pour tous les véhicules !');
        }
    });
}

// Filter vehicles based on status
function filterVehicles(filter) {
    const tbody = document.getElementById('vehicleMonitoring');
    const rows = tbody.querySelectorAll('tr');
    
    rows.forEach(row => {
        const statusBadge = row.querySelector('.badge');
        const statusText = statusBadge ? statusBadge.textContent.trim() : '';
        
        switch(filter) {
            case 'Tous':
                row.style.display = '';
                break;
            case 'Alertes':
                row.style.display = statusText.includes('Fatigue') || statusText.includes('Somnolence') ? '' : 'none';
                break;
            case 'Critiques':
                row.style.display = statusText.includes('Critique') ? '' : 'none';
                break;
        }
    });
}

// Export functionality
function exportReport() {
    const data = {
        timestamp: new Date().toISOString(),
        vehicles: [],
        alerts: [],
        summary: {
            totalVehicles: 24,
            alertsToday: 7,
            criticalIncidents: 2,
            averageSpeed: 65
        }
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `somnocontrol-report-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// WebSocket connection for real-time data (simulation)
function initializeWebSocket() {
    // This would connect to your Python backend WebSocket
    // const ws = new WebSocket('ws://localhost:8000/ws');
    
    // Simulate WebSocket messages
    setInterval(() => {
        const mockData = {
            type: 'vehicle_update',
            vehicleId: 'TRK-' + String(Math.floor(Math.random() * 3) + 1).padStart(3, '0'),
            speed: Math.floor(Math.random() * 50) + 60,
            drowsinessLevel: Math.random(),
            location: 'A' + Math.floor(Math.random() * 10) + ', Km ' + Math.floor(Math.random() * 300),
            timestamp: new Date().toISOString()
        };
        
        handleWebSocketMessage(mockData);
    }, 2000);
}

// Handle WebSocket messages
function handleWebSocketMessage(data) {
    switch(data.type) {
        case 'vehicle_update':
            updateVehicleStatus(data);
            break;
        case 'drowsiness_alert':
            handleDrowsinessAlert(data);
            break;
        case 'speed_violation':
            handleSpeedViolation(data);
            break;
    }
}

// Update vehicle status from WebSocket
function updateVehicleStatus(data) {
    // Update the monitoring table with real data from Arduino sensors
    console.log('Vehicle update received:', data);
}

// Handle drowsiness alerts
function handleDrowsinessAlert(data) {
    if (data.severity === 'critical') {
        showEmergencyModal();
    }
    addRecentAlert(data);
}

// Handle speed violations
function handleSpeedViolation(data) {
    addRecentAlert(data);
}

// Add recent alert to sidebar
function addRecentAlert(alertData) {
    const alertsContainer = document.querySelector('.card-body');
    const newAlert = document.createElement('div');
    newAlert.className = 'alert-item border-start border-danger border-4 ps-3 mb-3';
    newAlert.innerHTML = `
        <div class="d-flex justify-content-between">
            <small class="text-muted">À l'instant</small>
            <span class="badge bg-danger">Critique</span>
        </div>
        <strong>${alertData.vehicleId} - ${alertData.driverName}</strong>
        <p class="mb-1">${alertData.message}</p>
        <small class="text-muted">${alertData.location}</small>
    `;
    
    alertsContainer.insertBefore(newAlert, alertsContainer.firstChild);
    
    // Remove oldest alert if more than 5
    const alerts = alertsContainer.querySelectorAll('.alert-item');
    if (alerts.length > 5) {
        alerts[alerts.length - 1].remove();
    }
}

// Initialize WebSocket when page loads
// initializeWebSocket();