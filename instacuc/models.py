from datetime import datetime

from instacuc import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    img_file_name = db.Column(db.String(200))
    hidden_message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    has_hidden_message = db.Column(db.Boolean, default=False)
    fake = db.Column(db.Boolean, default=False)
