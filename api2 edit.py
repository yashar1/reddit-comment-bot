from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

#STUDENTS = {
 # '1': {'name': 'Mark', 'age': 100, 'spec': 'science'},
  #'2': {'name': 'Jane', 'age': 20, 'spec': 'biology'},
  #'3': {'name': 'Peter', 'age': 21, 'spec': 'history'},
  #'4': {'name': 'Kate', 'age': 22, 'spec': 'science'},
#}

STUDENTS = {
    '1': {'name': 'Oh yeah? Well the jerk store called, theyre running out of you!'},
    '2': {'name': 'Yadda Yadda Yadda'},
    '3': {'name': 'I said eeeeeeeassssssyyyy there, big fella!'},
}

parser = reqparse.RequestParser()

class StudentList(Resource):
  def get(self):
    return STUDENTS

def post(self):
    parser.add_argument("name")
    #parser.add_argument("age")
    #parser.add_argument("spec")
    args = parser.parse_args()
    student_id = int(max(STUDENTS.keys())) + 1
    student_id = '%i' % student_id
    STUDENTS[student_id] ={
        "name": args["name"],
        #"age": args["age"],
        #"spec": args["spec"],
    }
    return STUDENTS[student_id], 201

api.add_resource(StudentList, '/students')

if __name__=="_main__":
  app.run(debug=True)






















if __name__ == "__main__":
  app.run(debug=True)