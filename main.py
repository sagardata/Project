from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo

import urllib.parse

import openai

openai.api_key = "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"




app = Flask(__name__)
# Properly escape the username and password
username = urllib.parse.quote_plus("mrsagar1709")
password = urllib.parse.quote_plus("3ICREKBO8jedVINx")
app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@mydata.7swjzrf.mongodb.net/chatGPT"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats = myChats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question":question , "answer" : f"{chat['answer']}"}
            return jsonify(data)
        else:
            
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                        "role": "user",
                        "content": question
                        }
                    ],
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
            data = {"question": question, "answer": response["choices"][0]["message"]["content"]}
            mongo.db.chats.insert_one({"question": question, "answer": response["choices"][0]["message"]["content"]})
            return jsonify(data)      
    data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss? "}
        
    return jsonify(data)

app.run(debug=True, port=5001)










