// Reports Page JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    setupEventListeners();
    updateCurrentDate();
});

// Initialize all charts
function initializeCharts() {
    initializeDrowsinessChart();
    initializeSpeedChart();
}

// Drowsiness Trend Chart
function initializeDrowsinessChart() {
    const ctx = document.getElementById('drowsinessChart').getContext('2d');
    
    window.drowsinessChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            datasets: [{
                label: 'Incidents Mineurs',
                data: [2, 3, 1, 4, 2, 3, 1],
                borderColor: '#ffc107',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Incidents Modérés',
                data: [1, 2, 0, 3, 1, 2, 1],
                borderColor: '#fd7e14',
                backgroundColor: 'rgba(253, 126, 20, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Incidents Critiques',
                data: [0, 1, 0, 2, 1, 1, 0],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Speed Violations Chart
function initializeSpeedChart() {
    const ctx = document.getElementById('speedChart').getContext('2d');
    
    window.speedChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['TRK-001\n(Jean)', 'TRK-002\n(Marie)', 'TRK-003\n(Pierre)'],
            datasets: [{
                label: 'Violations Mineures (5-10 km/h)',
                data: [3, 8, 15],
                backgroundColor: 'rgba(255, 193, 7, 0.8)',
                borderColor: '#ffc107',
                borderWidth: 1
            }, {
                label: 'Violations Majeures (>10 km/h)',
                data: [1, 4, 8],
                backgroundColor: 'rgba(220, 53, 69, 0.8)',
                borderColor: '#dc3545',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 0
                    }
                }
            }
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    // Period filter change
    document.getElementById('periodFilter').addEventListener('change', function() {
        const customDateRange = document.getElementById('customDateRange');
        if (this.value === 'custom') {
            customDateRange.style.display = 'block';
        } else {
            customDateRange.style.display = 'none';
        }
    });
    
    // All vehicles checkbox
    document.getElementById('allVehicles').addEventListener('change', function() {
        const vehicleChecks = document.querySelectorAll('.vehicle-check');
        vehicleChecks.forEach(check => {
            check.checked = this.checked;
            check.disabled = this.checked;
        });
    });
    
    // Individual vehicle checkboxes
    document.querySelectorAll('.vehicle-check').forEach(check => {
        check.addEventListener('change', function() {
            const allVehicles = document.getElementById('allVehicles');
            const checkedBoxes = document.querySelectorAll('.vehicle-check:checked');
            const totalBoxes = document.querySelectorAll('.vehicle-check');
            
            if (checkedBoxes.length === totalBoxes.length) {
                allVehicles.checked = true;
            } else {
                allVehicles.checked = false;
            }
        });
    });
}

// Apply filters function
function applyFilters() {
    const period = document.getElementById('periodFilter').value;
    const reportType = document.getElementById('reportType').value;
    const vehicle = document.getElementById('vehicleFilter').value;
    
    // Show loading indicator
    showLoadingIndicator();
    
    // Simulate API call
    setTimeout(() => {
        updateChartsWithFilters(period, reportType, vehicle);
        hideLoadingIndicator();
        showToast('Filtres appliqués avec succès', 'success');
    }, 1500);
}

// Update charts with filters
function updateChartsWithFilters(period, reportType, vehicle) {
    // Update drowsiness chart based on filters
    if (reportType === 'all' || reportType === 'drowsiness') {
        updateDrowsinessChartData(period, vehicle);
    }
    
    // Update speed chart based on filters
    if (reportType === 'all' || reportType === 'speed') {
        updateSpeedChartData(period, vehicle);
    }
}

// Update drowsiness chart data
function updateDrowsinessChartData(period, vehicle) {
    const chart = window.drowsinessChart;
    
    // Simulate different data based on period
    let newData;
    switch(period) {
        case 'today':
            chart.data.labels = ['00h', '04h', '08h', '12h', '16h', '20h'];
            newData = {
                minor: [0, 1, 0, 2, 3, 1],
                moderate: [0, 0, 0, 1, 2, 0],
                critical: [0, 0, 0, 0, 1, 0]
            };
            break;
        case 'month':
            chart.data.labels = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'];
            newData = {
                minor: [8, 12, 6, 10],
                moderate: [3, 5, 2, 4],
                critical: [1, 2, 1, 1]
            };
            break;
        default: // week
            chart.data.labels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
            newData = {
                minor: [2, 3, 1, 4, 2, 3, 1],
                moderate: [1, 2, 0, 3, 1, 2, 1],
                critical: [0, 1, 0, 2, 1, 1, 0]
            };
    }
    
    chart.data.datasets[0].data = newData.minor;
    chart.data.datasets[1].data = newData.moderate;
    chart.data.datasets[2].data = newData.critical;
    
    chart.update();
}

// Update speed chart data
function updateSpeedChartData(period, vehicle) {
    const chart = window.speedChart;
    
    // Filter by vehicle if specified
    if (vehicle !== 'all') {
        // Show data for single vehicle
        chart.data.labels = [vehicle];
        chart.data.datasets[0].data = [Math.floor(Math.random() * 10) + 1];
        chart.data.datasets[1].data = [Math.floor(Math.random() * 5) + 1];
    } else {
        // Show data for all vehicles
        chart.data.labels = ['TRK-001\n(Jean)', 'TRK-002\n(Marie)', 'TRK-003\n(Pierre)'];
        chart.data.datasets[0].data = [3, 8, 15];
        chart.data.datasets[1].data = [1, 4, 8];
    }
    
    chart.update();
}

// Switch chart view (daily/weekly/monthly)
function switchChart(view) {
    // Update active button
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Update chart based on view
    updateDrowsinessChartData(view, 'all');
}

// Generate new report
function generateReport() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('generateReportModal'));
    modal.hide();
    
    // Show progress notification
    showProgressToast('Génération du rapport en cours...', 'info');
    
    // Simulate report generation
    setTimeout(() => {
        showToast('Rapport généré avec succès!', 'success');
        addNewReportToList();
    }, 3000);
}

// Add new report to the list
function addNewReportToList() {
    const reportsContainer = document.querySelector('.card-body');
    const newReport = document.createElement('div');
    newReport.className = 'report-item mb-3 p-3 border rounded';
    newReport.innerHTML = `
        <div class="d-flex justify-content-between align-items-start mb-2">
            <h6 class="mb-0">Nouveau Rapport</h6>
            <span class="badge bg-success">Complété</span>
        </div>
        <p class="text-muted small mb-2">Rapport généré à la demande</p>
        <div class="d-flex justify-content-between align-items-center">
            <small class="text-muted">
                <i class="fas fa-calendar me-1"></i>À l'instant
            </small>
            <div class="btn-group btn-group-sm">
                <button class="btn btn-outline-primary" onclick="viewReport('new')">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-outline-secondary" onclick="downloadReport('new')">
                    <i class="fas fa-download"></i>
                </button>
            </div>
        </div>
    `;
    
    reportsContainer.insertBefore(newReport, reportsContainer.firstChild);
}

// View report
function viewReport(reportId) {
    showToast('Ouverture du rapport...', 'info');
    // Simulate opening report in new tab
    // window.open(`/reports/${reportId}`, '_blank');
}

// Download report
function downloadReport(reportId) {
    showProgressToast('Téléchargement en cours...', 'info');
    
    // Simulate download
    setTimeout(() => {
        const link = document.createElement('a');
        link.href = '#'; // This would be the actual report URL
        link.download = `somnocontrol-report-${reportId}-${new Date().toISOString().split('T')[0]}.pdf`;
        link.click();
        showToast('Rapport téléchargé!', 'success');
    }, 1500);
}

// Export data function
function exportData() {
    const format = document.getElementById('exportFormat').value;
    const includeCharts = document.getElementById('includeCharts').checked;
    const includeDetails = document.getElementById('includeDetails').checked;
    const includeRecommendations = document.getElementById('includeRecommendations').checked;
    
    showProgressToast(`Export en format ${format.toUpperCase()} en cours...`, 'info');
    
    // Simulate export process
    setTimeout(() => {
        const exportData = {
            format: format,
            timestamp: new Date().toISOString(),
            includeCharts: includeCharts,
            includeDetails: includeDetails,
            includeRecommendations: includeRecommendations,
            data: {
                summary: {
                    totalAlerts: 47,
                    criticalDrowsiness: 12,
                    speedViolations: 23,
                    drivingHours: 168,
                    kilometers: 2847,
                    compliance: 94.2
                }
            }
        };
        
        // Create and download file
        const blob = new Blob([JSON.stringify(exportData, null, 2)], { 
            type: format === 'json' ? 'application/json' : 'text/plain' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `somnocontrol-export-${new Date().toISOString().split('T')[0]}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showToast(`Données exportées en ${format.toUpperCase()}!`, 'success');
    }, 2000);
}

// Update current date
function updateCurrentDate() {
    const dateElements = document.querySelectorAll('.text-muted');
    const currentDate = new Date().toLocaleString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // Update the first date element (page header)
    if (dateElements.length > 0) {
        dateElements[0].textContent = `Dernière mise à jour: ${currentDate}`;
    }
}

// Utility functions
function showLoadingIndicator() {
    const btn = document.querySelector('button[onclick="applyFilters()"]');
    btn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Chargement...';
    btn.disabled = true;
}

function hideLoadingIndicator() {
    const btn = document.querySelector('button[onclick="applyFilters()"]');
    btn.innerHTML = '<i class="fas fa-search me-2"></i>Appliquer';
    btn.disabled = false;
}

function showToast(message, type) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 3000);
}

function showProgressToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        <i class="fas fa-spinner fa-spin me-2"></i>${message}
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

// Auto-refresh data every 30 seconds
setInterval(() => {
    // Simulate real-time data updates
    updateChartsWithNewData();
}, 30000);

function updateChartsWithNewData() {
    // Add some random variation to existing data
    if (window.drowsinessChart) {
        const chart = window.drowsinessChart;
        chart.data.datasets.forEach(dataset => {
            dataset.data = dataset.data.map(value => 
                Math.max(0, value + Math.floor(Math.random() * 3) - 1)
            );
        });
        chart.update('none');
    }
}