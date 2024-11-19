document.addEventListener('DOMContentLoaded', () => {
    // Obtener los datos del backend
    fetch('/dashboard/api/')
        .then(response => response.json())
        .then(data => {
            // Renderizar los gráficos
            renderTasaOcupacionChart(data.tasa_ocupacion);
            renderReservasPorServicioChart(data.reservas_por_servicio);
            renderTasaPagoChart(data.tasa_pago);
            renderCrecimientoReservasChart(data.crecimiento_reservas);
            renderProductosUtilizadosChart(data.productos_utilizados);
            renderCostosPorServicioChart(data.costos_por_servicio);
        })
        .catch(error => {
            console.error("Error al cargar los datos del dashboard:", error);
        });
});

// Tasa de Ocupación
function renderTasaOcupacionChart(tasaOcupacion) {
    const ctx = document.getElementById('tasaOcupacionChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Ocupado', 'Disponible'],
            datasets: [{
                data: [tasaOcupacion, 100 - tasaOcupacion],
                backgroundColor: ['#117391', '#D7D7D7'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tasa de Ocupación (%)'
                }
            }
        }
    });
}

// Reservas por Servicio
function renderReservasPorServicioChart(reservasPorServicio) {
    const ctx = document.getElementById('reservasPorServicioChart').getContext('2d');
    const labels = reservasPorServicio.map(item => item.id_servicio__tipo_servicio);
    const data = reservasPorServicio.map(item => item.total);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Número de Reservas',
                data: data,
                backgroundColor: '#16BFE8'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Reservas por Servicio'
                }
            }
        }
    });
}

// Tasa de Pago Completado
function renderTasaPagoChart(tasaPago) {
    const ctx = document.getElementById('tasaPagoChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Pagado', 'Pendiente'],
            datasets: [{
                data: [tasaPago, 100 - tasaPago],
                backgroundColor: ['#117391', '#D7D7D7']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tasa de Pago Completado (%)'
                }
            }
        }
    });
}

// Crecimiento de Reservas
function renderCrecimientoReservasChart(crecimientoReservas) {
    const ctx = document.getElementById('crecimientoReservasChart').getContext('2d');
    const labels = crecimientoReservas.map(item => item.month);
    const data = crecimientoReservas.map(item => item.total);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Crecimiento de Reservas',
                data: data,
                borderColor: '#16BFE8',
                backgroundColor: 'rgba(22, 191, 232, 0.2)',
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Crecimiento de Reservas Mensual'
                }
            }
        }
    });
}

// Productos Más Utilizados
function renderProductosUtilizadosChart(productosUtilizados) {
    const ctx = document.getElementById('productosUtilizadosChart').getContext('2d');
    const labels = productosUtilizados.map(item => item.id_producto__nombre_producto);
    const data = productosUtilizados.map(item => item.total_usado);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Uso de Productos',
                data: data,
                backgroundColor: '#117391'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Productos Más Utilizados'
                }
            }
        }
    });
}

// Costos por Servicio
function renderCostosPorServicioChart(costosPorServicio) {
    const ctx = document.getElementById('costosPorServicioChart').getContext('2d');
    const labels = costosPorServicio.map(item => item.id_servicio__tipo_servicio);
    const dataInsumos = costosPorServicio.map(item => item.costo_insumos || 0);
    const dataManoObra = costosPorServicio.map(item => item.costo_mano_obra || 0);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Costo de Insumos',
                    data: dataInsumos,
                    backgroundColor: '#16BFE8'
                },
                {
                    label: 'Costo de Mano de Obra',
                    data: dataManoObra,
                    backgroundColor: '#117391'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Costos por Servicio'
                }
            }
        }
    });
}
