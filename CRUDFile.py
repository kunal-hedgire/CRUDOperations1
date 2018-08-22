from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
#import openpyxl


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Register.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    address = db.Column(db.String(100))
    password = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    yearofexp = db.Column(db.Integer)
    skill = db.Column(db.String(10))

    def __init__(self,fname,lname,age,addr,pas,gen,yrexpr,skill):
        self.firstname=fname
        self.lastname=lname
        self.age=age
        self.address=addr
        self.password=pas
        self.gender=gen
        self.yearofexp=yrexpr
        self.skill=skill


def excelOperation(datalist):
    pass


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(request.form['firstname'],
                    request.form['lastname'],
                    request.form['age'],
                    request.form['address'],
                    request.form['password'],
                    request.form['gender'],
                    request.form['yearofexp'],
                    request.form['java'])
        db.session.add(user)
        db.session.commit()
        return render_template('login.html', msg="success")

    nmsg = request.args.get('msg')

    return render_template('login.html',msg = nmsg)


@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        updateuser = User.query.filter_by(id=request.form['editid']).first()
        updateuser.firstname = request.form['firstname']
        updateuser.lastname = request.form['lastname']
        updateuser.age = request.form['age']
        updateuser.address = request.form['address']
        updateuser.password = request.form['password']
        updateuser.gender = request.form['gender']
        updateuser.yearofexp = request.form['yearofexp']
        updateuser.java = request.form['java']
        db.session.commit()
        userlist = User.query.all()
        return render_template('showdata.html', msg="User is Updated", records=userlist)
    uid = request.args.get('id')
    uinfo = User.query.filter_by(id=uid).all()
    return render_template('registration.html',edituser=uinfo)


@app.route('/showdata',methods=['GET','POST'])
def showdata():
    if request.method == 'POST':
        print(request.form)
        ulist = User.query.filter_by(address= request.form['username']).all()
        for u in ulist:
            if u.address==request.form['username'] and u.password==request.form['password']:
                userlist = User.query.all()
                return render_template('showdata.html', records = userlist)
    uid = request.args.get('delid')
    data = request.args.get('data')
    if uid :
        deleteuser = User.query.filter_by(id=uid).first()
        db.session.delete(deleteuser)
        db.session.commit()
        userlist = User.query.all()
        return render_template('showdata.html', msg = "User is Deleted", records = userlist)
    elif data:
        print("**********************************************************************")
        datalist = []
        for obj in data:
            print(obj)
            #datalist.append([obj.firstname, obj.lastname, obj.age, obj.address, obj.gender, obj.yearofexp, obj.java ])
        print(datalist)
        userlist = User.query.all()
        return render_template('showdata.html', msg="Data is exported", records=userlist)
    else:
        #return render_template('login.html',msg="Invalid Credentials")
        return redirect(url_for('login', msg="Invalid Credentials"))


if __name__ == '__main__':
   db.create_all()
   app.run(debug=True,port=8081)
