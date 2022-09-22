from crypt import methods

from flask import Flask, request, jsonify

from flask_pymongo import PyMongo, ObjectId
from bson import json_util

app = Flask(__name__)

app.config['Mongo_URI']= 'mongodb://localhost:27017/base'

mongo = PyMongo(app)


dbu=mongo.db.users
dbc=mongo.db.clubs


@app.route('/users/<user>,<password>,<names>,<lastnames>,<section>,<isAdmin>', methods=['POST'])
def createUser( user, 
                password, 
                names, 
                lastnames, 
                section, 
                isAdmin
                ):
    #datos
    #usuario, password,nombres, apellidos, seccion, esAdmin
    id=dbu.insert({'user':user,
                    'password':password,
                    'names':names,
                    'lastnames':lastnames,
                    'section':section,
                    'isAdmin':isAdmin
                    })
    
    return jsonify(str(ObjectId(id)))

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user=dbu.find_one({'_id':ObjectId(id)})
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
        'names': user['names'],
        'user':user['user'],
        'password':user['password'],
        'lastnames':user['lastnames'],
        'section':user['section'],
        'isAdmin':user['isAdmin'],
        })


@app.route('/users/<id>', methods=['DELETE'])
def deleteUsers(id):
    dbu.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User deleted'})


@app.route('/users', methods=['GET'])
def getUsers():
    users=[]
    for doc in dbu.find():
        users.append({
            '_id':str(ObjectId(doc['_id'])),
            'user': doc['user'],
            'names':doc['names'],
            'password':doc['password'],
            'lastnames':doc['lastnames'],
            'section':doc['section'],
            'isAdmin':doc['isAdmin']
        })
    return jsonify(users)

@app.route('/clubs/<name>,<category>,<followers>', methods=['POST'])
def createClub(name,category,followers):
    #datos
    #nombre,categoria,seguidores(id de usuarios)
    id=dbc.insert({'name':name,
                    'category':category,
                    'followers':followers
                    
                    })
    return jsonify(str(ObjectId(id)))

@app.route('/clubs/<id>,<idUser>', methods=['PUT'])
def updateFollowers(id):
    dbc.update_one({'_id': ObjectId(id)},
    {'$set':{
        'followers': request.json['idUser']     
    }})
    return jsonify({'msg': 'User updated'})

##comprobar club, si devuelve algo se debe hacer el metodo en el fe para que lo descarte y tire error
@app.route('/clubs/<name>,<category>', methods=['GET'])
def getClubsTop():
    clubs=[]
    for doc in dbc.find():
        clubs.append({
            '_id':str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'category':doc['category'],
            'followers':doc['followers'] #Hacer un conteo en el fe          
        })
    return jsonify(clubs)




@app.route('/clubs/<id>', methods=['DELETE'])
def deleteClub(id):
    dbc.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Club deleted'})

# Cantidad total de clubes distintos
# sugeridos por los estudiantes, según la 
#categoría. Por ejemplo: 30 clubes de arte,
#  10 de deportes, etc.
@app.route('/clubs', methods=['GET'])
def getClubs():
    clubs=[]
    for doc in dbc.find():
        clubs.append({
            '_id':str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'category':doc['category'],
            'followers':doc['followers']
            
        })
    return jsonify(clubs)
   
#Mostrar el nombre completo y la cantidad de
#  clubes sugeridos para lostres estudiantes
#  que más sugerencias hayan realizado.

###conteo de todos los id de los clubes que mas se repitan
####Tomaríamos el id de la lista de followers de los clubes
@app.route('/users/<id>', methods=['GET'])
def getUsersTop(id):

    user=dbu.find_one({'_id':ObjectId(id)})
    return jsonify({
        '_id':str(ObjectId(user['_id'])),
        'names': user['names'],     
        'lastnames':user['lastnames']  
        })

#Top 5 de clubes sugeridos. Se debe mostrar una
#  lista de los cinco clubes más solicitados,
#  incluyendo el nombre del club, la categoría
#  y la cantidad de veces que fue sugerido.
@app.route('/clubs/<id>', methods=['GET'])
def getClubsTop():
    clubs=[]
    for doc in dbc.find():
        clubs.append({
            '_id':str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'category':doc['category'],
            'followers':doc['followers'] #Hacer un conteo en el fe          
        })
    return jsonify(clubs)

#Bottom 3 de clubes sugeridos. Se debe mostrar una
#lista de los cinco clubes menos solicitados,
#incluyendo el nombre del club, la categoría y 
#la cantidad de veces que fue sugerido.

##??????

if __name__ == '__main__':
    app.run(debug=True)
