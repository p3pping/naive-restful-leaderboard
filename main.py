from flask import Flask
from flask_restful import Api, Resource, reqparse
import uuid

app = Flask(__name__)
api = Api(app)

#constants
C_UID = "uid"
C_USERNAME = "username"
C_SCORE = "score"
C_NEW = "new"

scores_db = [
    {
        C_UID: str(uuid.uuid4()),
        C_USERNAME: "Yulee",
        C_SCORE: 12
    },
    {
        C_UID: str(uuid.uuid4()),
        C_USERNAME: "Michael",
        C_SCORE: 10
    }
]

class HighScore(Resource):

    def create_score(self, uid, username, score):
        return { 
            C_UID: uid,
            C_USERNAME: username,
            C_SCORE: score
        }

    #finds and returns an existing user
    def get(self, uid):
        for s in scores_db:
            if s[C_UID] == uid:
                return s, 200
        return "User not found", 404
    
    #creates a new user if it doesnt exist
    def post(self, uid):
        #parse out arguments
        parser = reqparse.RequestParser()
        parser.add_argument(C_USERNAME)
        parser.add_argument(C_SCORE)
        args = parser.parse_args()        

        #if it does exists then exit out
        for s in scores_db:
            if s[C_UID] == uid:
                return "User already exists", 400

        #if it doesnt exist then create and return the new high score 
        new_score = self.create_score(str(uuid.uuid4()), args[C_USERNAME], args[C_SCORE])

        scores_db.append(new_score)
        return new_score, 201
    
    def put(self, uid):
        #parse out arguments
        parser = reqparse.RequestParser()
        parser.add_argument(C_USERNAME)
        parser.add_argument(C_SCORE)
        args = parser.parse_args()
        
        #if it exists update it
        for s in scores_db:
            if s[C_UID] == uid:
                s[C_SCORE] = args[C_SCORE]
                s[C_USERNAME] = args[C_USERNAME]
                return s, 200

        #if it doesnt exists create it 
        new_score = self.create_score(str(uuid.uuid4()), args[C_USERNAME], args[C_SCORE])

        scores_db.append(new_score)
        return new_score, 201
    
    def delete(self, uid):
        return "Deleted", 200
    
if __name__ == "__main__":    
    api.add_resource(HighScore, "/score/<string:uid>")
    app.run(debug=True)


    