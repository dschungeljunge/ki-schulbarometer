from database import db

class Teilnehmer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alter = db.Column(db.Integer)
    berufserfahrung = db.Column(db.Integer)
    geschlecht = db.Column(db.String(20))
    schulstufe = db.Column(db.String(50))
    funktionen = db.Column(db.String(100))
    antworten = db.Column(db.PickleType)
