from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Configurar la base de datos
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS startups (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            sector TEXT NOT NULL,
                            funding INTEGER NOT NULL,
                            team INTEGER NOT NULL
                        )''')
    print("Base de datos inicializada.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_startup', methods=['POST'])
def add_startup():
    data = request.json
    name = data['name']
    sector = data['sector']
    funding = data['funding']
    team = data['team']
    
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO startups (name, sector, funding, team) VALUES (?, ?, ?, ?)",
                    (name, sector, funding, team))
        conn.commit()
        startup_id = cur.lastrowid
    
    return jsonify(id=startup_id)

def calculate_success_probability(sector, funding, team):
    # Pesos para diferentes factores
    sector_weights = {
        'tecnología': 1.2,
        'salud': 1.1,
        'educación': 1.0,
        'comercio': 0.9,
        'otro': 0.8
    }
    
    # Asignar un puntaje basado en el sector
    sector_score = sector_weights.get(sector.lower(), 0.8)
    
    # Normalizar financiamiento y tamaño del equipo
    funding_score = min(funding / 10000, 1)
    team_score = min(team / 10, 1)
    
    # Calcular el puntaje total
    total_score = (0.4 * sector_score) + (0.3 * funding_score) + (0.3 * team_score)
    
    # Convertir el puntaje a una probabilidad
    success_probability = total_score * 100
    return success_probability

@app.route('/forecast', methods=['POST'])
def forecast():
    data = request.json
    name = data['name']
    sector = data['sector']
    funding = data['funding']
    team = data['team']
    
    success_probability = calculate_success_probability(sector, funding, team)
    result = f"La startup {name} en el sector {sector} tiene una probabilidad de éxito del {success_probability:.2f}%."
    
    if success_probability < 50:
        result += " Se recomienda buscar más financiamiento o aumentar el tamaño del equipo."
    elif success_probability < 75:
        result += " El pronóstico es moderadamente favorable."
    else:
        result += " El pronóstico es altamente favorable."

    return jsonify(result=result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
