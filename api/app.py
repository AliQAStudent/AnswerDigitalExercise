from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import json
from collections import namedtuple
import create_db

import sqlite3

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Tech Test API"
    }
)
app.register_blueprint(swaggerui_blueprint)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/api/people")
def getall_people():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_people = cur.execute('SELECT * FROM Person;').fetchall()
    return jsonify(all_people)

# GET /api/person/{id} - get person with given id
@app.route("/api/person/<id>")
def get_one_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    person = cur.execute('SELECT * FROM Person WHERE id = '+id+';').fetchall()
    return jsonify(person)

# PUT /api/person/{id} - Update a person with the given id
@app.route("/api/person/<id>", methods = ['PUT'])
def update_one_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    conn.execute('UPDATE Person SET authorised = '+request.args.get("authorised")+', enabled='+request.args.get("enabled")+', firstName = \''+request.args.get("firstName")+'\', lastName=\''+request.args.get("lastName")+'\' WHERE id = '+id+';')
    conn.commit()
    return "done"

# DELETE /api/person/{id} - Delete a person with a given id
@app.route("/api/person/<id>", methods = ['DELETE'])
def delete_one_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    conn.execute('DELETE FROM Person WHERE id = '+id+';')
    conn.commit()
    return "done"

# POST /api/people - create 1 person. Takes in a json body
@app.route("/api/people", methods = ['POST'])
def create_one_person():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    requestString = request.data.decode("utf-8")
    requestJSONObject = x = json.loads(requestString, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    conn.execute('INSERT INTO Person (authorised, enabled, firstName, lastName) VALUES ('+str(requestJSONObject.authorised)+','+str(requestJSONObject.enabled)+',\''+requestJSONObject.firstName+'\',\''+requestJSONObject.lastName+'\')')
    conn.commit()
    return "done"

if __name__ == '__main__':
    app.run()
