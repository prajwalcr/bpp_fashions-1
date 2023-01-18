from flaskapp import db


class Product(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    availability = db.Column(db.Boolean)
    productDescription = db.Column(db.Text)
    imageURL = db.Column(db.Text)
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Product('{self.id}, '{self.price}')"
