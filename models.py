from app import db


class Users(db.Model):
    identifier = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True,
                           unique=True,
                           nullable=False)
    email = db.Column(db.String(30),
                      unique=True,
                      nullable=False)
    login = db.Column(db.String(30),
                      unique=True,
                      nullable=False,
                      )
    password = db.Column(db.String(30),
                         nullable=False)


class Products(db.Model):
    product_identifier = db.Column(db.Integer,
                                   primary_key=True,
                                   autoincrement=True,
                                   unique=True,
                                   nullable=False)
    product_type = db.Column(db.String(30),
                             nullable=False)
    product_name = db.Column(db.String(30),
                             nullable=False)
    product_description = db.Column(db.String(100),
                                    nullable=False)
    product_brand = db.Column(db.String(30),
                              nullable=False)
    product_price = db.Column(db.Integer,
                              nullable=False)
