from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from database import db
from models import Teilnehmer
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:UWvqnlkEuSYaxUrWPDWMHjneHzYAxBOF@postgres.railway.internal:5432/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

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

        # Fragebogen-Antworten werden direkt gespeichert
        frage1 = int(request.form.get('frage1'))
        frage2 = int(request.form.get('frage2'))
        frage3 = int(request.form.get('frage3'))
        frage4 = int(request.form.get('frage4'))
        frage5 = int(request.form.get('frage5'))
        frage6 = int(request.form.get('frage6'))
        frage7 = int(request.form.get('frage7'))
        frage8 = int(request.form.get('frage8'))
        frage9 = int(request.form.get('frage9'))
        frage10 = int(request.form.get('frage10'))
        frage11 = int(request.form.get('frage11'))
        frage12 = int(request.form.get('frage12'))
        frage13 = int(request.form.get('frage13'))
        frage14 = int(request.form.get('frage14'))
        frage15 = int(request.form.get('frage15'))
        frage16 = int(request.form.get('frage16'))
        frage17 = int(request.form.get('frage17'))
        frage18 = int(request.form.get('frage18'))
        frage19 = int(request.form.get('frage19'))
        frage20 = int(request.form.get('frage20'))
        frage21 = int(request.form.get('frage21'))

        # Neuen Teilnehmer in die Datenbank einfügen
        teilnehmer = Teilnehmer(
            alter=alter,
            berufserfahrung=berufserfahrung,
            geschlecht=geschlecht,
            schulstufe=schulstufe,
            funktionen=funktionen,
            frage1=frage1, frage2=frage2, frage3=frage3, frage4=frage4, frage5=frage5,
            frage6=frage6, frage7=frage7, frage8=frage8, frage9=frage9, frage10=frage10,
            frage11=frage11, frage12=frage12, frage13=frage13, frage14=frage14, frage15=frage15,
            frage16=frage16, frage17=frage17, frage18=frage18, frage19=frage19, frage20=frage20,
            frage21=frage21
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
