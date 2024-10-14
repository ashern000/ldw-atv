# app.py
from flask import Flask, request
from flask_restful import Api, Resource
from schemas import TaskSchema
from models import mongo_db

app = Flask(__name__)
api = Api(app)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class TaskResource(Resource):
    def get(self, task_id=None):
        if task_id:
            task = mongo_db.collection.find_one({"_id": task_id})
            if task:
                return task_schema.dump(task), 200
            return {"message": "Task not found"}, 404
        tasks = list(mongo_db.collection.find())
        return tasks_schema.dump(tasks), 200

    def post(self):
        print("Corpo da requisição:", request.data)  # Adicione esta linha para imprimir o corpo da requisição
        json_data = request.get_json()
        
        if json_data is None:
            return {"message": "Failed to decode JSON object."}, 400

        print("Dados decifrados:", json_data)  # Adicione esta linha para imprimir os dados decifrados

        errors = task_schema.validate(json_data)
        if errors:
            print("Erros de validação:", errors)  # Adicione esta linha para imprimir erros de validação
            return errors, 400

        task = {
            "title": json_data["title"],
            "description": json_data["description"],
        }
        mongo_db.collection.insert_one(task)
        return task_schema.dump(task), 201



    def put(self, task_id):
        json_data = request.get_json()
        errors = task_schema.validate(json_data)
        if errors:
            return errors, 400

        result = mongo_db.collection.update_one({"_id": task_id}, {"$set": json_data})
        if result.matched_count == 0:
            return {"message": "Task not found"}, 404
        
        return task_schema.dump(json_data), 200

    def delete(self, task_id):
        result = mongo_db.collection.delete_one({"_id": task_id})
        if result.deleted_count == 0:
            return {"message": "Task not found"}, 404
        
        return {"message": "Task deleted"}, 204

api.add_resource(TaskResource, "/tasks", "/tasks/<string:task_id>")

if __name__ == "__main__":
    app.run(debug=True)
