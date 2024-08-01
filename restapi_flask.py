from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("<your_mongo_uri>")
db = client.sos_database
collection = db.sos_collection

class SOSResource(Resource):
    def get(self):
        selected_semester = request.args.get('selected_semester')
        if selected_semester:
            courses = collection.find({'selected_semester': selected_semester})
            return jsonify({'courses': [course['course_info'] for course in courses]})
        else:
            return jsonify({'error': 'Please provide a valid semester.'})

    def post(self):
        data = request.get_json()
        course_info = f"{data['subject_name']}: {data['description']} ({data['course_code']}, {data['teacher_name']})"
        data['course_info'] = course_info
        collection.insert_one(data)
        return jsonify({'message': 'Item added successfully.'})

    def delete(self):
        data = request.args.get('selected_item')
        selected_semester = request.args.get('selected_semester')
        if data and selected_semester:
            collection.delete_one({'course_info': data, 'selected_semester': selected_semester})
            return jsonify({'message': 'Item deleted successfully.'})
        else:
            return jsonify({'error': 'Please provide a valid item and semester.'})

api.add_resource(SOSResource, '/sos')

if __name__ == '__main__':
    app.run(debug=True)