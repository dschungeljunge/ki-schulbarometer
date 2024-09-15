from flask import Flask, render_template, request, redirect, url_for
from database import db  # db aus database.py importieren
from models import Teilnehmer
import json  # Für die Konvertierung von Antworten
import pandas as pd
import numpy as np

# Flask-App erstellen
app = Flask(__name__)

# SQLAlchemy konfigurieren (Datenbankverbindung)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datenbank.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dschungeljunge:PHhsluuni8102@junction.proxy.rlwy.net:33275/junction.proxy.rlwy.net'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Funktionen für Datenanalyse und Statistiken
def hole_daten():
    teilnehmer = Teilnehmer.query.all()
    daten = []
    for t in teilnehmer:
        # Antworten aus der Datenbank zurück in ein Dictionary konvertieren
        antworten_dict = json.loads(t.antworten)
        daten.append(antworten_dict)  # Hier nehmen wir an, dass "antworten" ein Dictionary ist
    df = pd.DataFrame(daten)
    return df

def berechne_statistiken(df):
    # Konvertiere alle Spalten zu numerischen Werten, falls nötig
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Beispiel: Mittelwerte berechnen
    mittelwerte = df.mean()
    return mittelwerte

# Routen
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # Persönliche Informationen
        alter = request.form.get('alter')
        berufserfahrung = request.form.get('berufserfahrung')
        geschlecht = request.form.get('geschlecht')
        schulstufe = request.form.get('schulstufe')
        funktionen = request.form.get('funktionen')

        # Fragebogen-Antworten
        antworten = {
            'pos1': request.form.get('pos1'),
            'pos2': request.form.get('pos2'),
            'neg3': request.form.get('neg3'),
            'neg6': request.form.get('neg6')
        }

        # Antworten werden als JSON gespeichert
        antworten_json = json.dumps(antworten)

        # Neuen Teilnehmer in die Datenbank einfügen
        teilnehmer = Teilnehmer(
            alter=alter,
            berufserfahrung=berufserfahrung,
            geschlecht=geschlecht,
            schulstufe=schulstufe,
            funktionen=funktionen,
            antworten=antworten_json  # Speichert die Antworten als JSON
        )
        db.session.add(teilnehmer)
        db.session.commit()

        # Weiterleitung zur Ergebnis-Seite
        return redirect(url_for('ergebnis'))

    # GET-Request: Das Formular anzeigen
    return render_template('test.html')

@app.route('/ergebnis')
def ergebnis():
    teilnehmer = Teilnehmer.query.all()
    return render_template('ergebnis.html', teilnehmer=teilnehmer)

@app.route('/forschung')
def forschung():
    # Daten abrufen
    df = hole_daten()

    # Statistiken berechnen
    statistiken = berechne_statistiken(df)

    # Statistiken in ein Dictionary konvertieren, damit sie in HTML gerendert werden können
    statistiken_dict = statistiken.to_dict()

    # Ergebnisse in der HTML-Seite anzeigen
    return render_template('forschung.html', statistiken=statistiken_dict)

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

# Datenbanktabellen erstellen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
