from flask import Flask, jsonify, request
from passlib.hash import pbkdf2_sha256
# import env.app
# from env.app import db
import uuid

class User:
    def signup(self):
        # print(request.form)
        print("in signup function")
        # create user object
        admin = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }

        #encrypt password
        # admin['password'] = pbkdf2_sha256.encrypt(admin['password'])
        print(jsonify(admin))

        # save db
        db.admin1.insert_one(admin)

        #check email exists
        if(db.admin1.findOne({email: admin["email"]})):
            return jsonify({"error": "email exits"}), 400

        if(db.admin1.insert_one(admin)):
            return jsonify(admin), 200

        return jsonify({"error": "Signup failed"})