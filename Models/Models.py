from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


# #Create model for blog Contacts
class Posts(db.Model):
    __tablename__ = "tbl_post"
    sn = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=True)
    img_url = db.Column(db.String(50), unique=True, default='alt.jpg')
    muted_text = db.Column(db.String(200), unique=False, nullable=True)
    content = db.Column(db.String(), unique=True, nullable=True)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.now)
    created_by = db.Column(db.String(50), nullable=True)


# #Create model for blog Contacts
class Contacts(db.Model):
    __tablename__ = "tbl_contact"
    sn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    contact_no = db.Column(db.String(12), unique=True, nullable=False)
    message = db.Column(db.String(), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    created_by = db.Column(db.String(50), nullable=True)


# Create  model for employee
class EmployeeModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    position = db.Column(db.String(80))

    def __init__(self, employee_id, name, age, position):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.position = position

    def __repr__(self):
        return f"{self.name}:{self.employee_id}"
