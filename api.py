from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

QUOTE = {
    '1': {'Quote': 'Oh yeah? Well the jerk store called, theyre running out of you!'},
    '2': {'Quote': 'Yadda Yadda Yadda'},
    '3': {'Quote': 'I said eeeeeeeassssssyyyy there, big fella!'},
}

parser = reqparse.RequestParser()

class QuoteList(Resource):
    def get(self):
        return QUOTE

    def post(self):
        parser.add_argument("Quote")
        args = parser.parse_args()
        quote_id = int(max(QUOTE.keys())) + 1
        quote_id = '%i' % quote_id
        QUOTE[quote_id] ={
            "Quote": args["Quote"]
        }
        return QUOTE[quote_id], 201


api.add_resource(QuoteList, '/quotes')

if __name__ == "_main__":
    app.run(debug=True)