from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)

# local postgres setup: app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost:5433/height_collector'

app.config['SQLALCHEMY_DATABASE_URI']='postgres://rmmutxreberlfx:decdf1d8ad3c398be9253c97031a34d9d4aef67dc970e64d0fc5e4c160201f77@ec2-107-22-160-199.compute-1.amazonaws.com:5432/dagcqg6ed9jh1n?sslmode=require'

db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

# to create database:
# command line: python
# from app (script name) import db
# db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=["POST"])
def success():
    if request.method=="POST":
        email=request.form['email_name']
        height=request.form['height_name']
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height,1)
            count=db.session.query(Data.height_).count()
            # send_email(email, height)
            return render_template("success.html", average=average_height, count=count)
        return render_template('index.html', text="ERROR: email address must be unique.")

if __name__ =='__main__':
    app.debug=True
    app.run()
