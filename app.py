import sys
from flask import Flask, request, render_template, jsonify
import pymongo
from env.users.models import User
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
import uuid

app = Flask(__name__)

# database
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/adminUser")
db = mongodb_client.db

# def init_db():
#     db.init_app(app)
#     db.app = app    
    

@app.route('/')
def home():
    return render_template("state.html")

@app.route('/analysis/')
def analysis():
    return render_template("analysis.html")

@app.route('/admin/login/', methods=['GET', 'POST'])
def admin():
    print('calling signup')
    User().signup()
    return render_template("admin.html") 

class User:
    def signup(self):
        # print(request.form)
        print("in signup function")
        # create user object
        admin = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        # print(jsonify(admin))
        #encrypt password
        hash_password = sha256_crypt.encrypt(admin['password'])
        admin['password'] = hash_password
        # print(jsonify(admin))

        # save db

        #check email exists
        if(db.admin1.find_one({"email" : admin['email']})):
            return jsonify({"error": "email exits"}), 400
        print("saving")
        db.admin1.save(admin)

            # return jsonify(admin), 200
        # db.admin1.insert_one(admin)
        

        return jsonify({"error": "Signup failed"})


if __name__ == "__main__":
    # app.init_db()
    app.run(debug=True)
    # app = create_app()
