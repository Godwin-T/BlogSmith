from chatbot import crew
from flask import Flask, request, jsonify


app = Flask("Blogsmith")


@app.route("/respond", methods=["POST"])
def respond():

    print("============================================")
    query = request.get_json()
    response = crew.kickoff(query)
    output = response.raw
    return jsonify({"response": output})


if __name__ == "__main__":
    app.run(debug=True, port=9696)
