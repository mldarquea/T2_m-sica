from my_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    subscriptions = db.relationship('Subscription', backref='subscribed', lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}')"


# Run migrations
db.create_all()
