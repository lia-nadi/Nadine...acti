async function submitForm() {
    const name = document.getElementById('name').value;
    const sector = document.getElementById('sector').value;
    const funding = document.getElementById('funding').value;
    const team = document.getElementById('team').value;
    
    // Registrar la startup en la base de datos
    await fetch('/add_startup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, sector, funding, team })
    });

    // Obtener el pronóstico
    const response = await fetch('/forecast', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, sector, funding, team })
    });

    const data = await response.json();
    document.getElementById('result').innerText = data.result;

    // Crear gráfico
    createChart(name, funding, team);
}

function createChart(name, funding, team) {
    const ctx = document.getElementById('funding-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Financiamiento Inicial', 'Número de Integrantes'],
            datasets: [{
                label: `Datos de ${name}`,
                data: [funding, team],
                backgroundColor: ['#007BFF', '#28A745'],
                borderColor: ['#007BFF', '#28A745'],
                borderWidth: 1
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
                    text: 'Distribución de Recursos de la Startup'
                }
            }
        }
    });
}
