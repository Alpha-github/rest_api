from flask import Flask, jsonify, request
import json
import os
import requests

app = Flask(__name__)

base_url  = "/api/v1"
data_path = f"{os.getcwd()}/data.json"

#print(os.environ['LOG_LEVEL'])
# GET
@app.route(f"{base_url}/")
def all():
    with open (data_path, 'r') as f:
        user_data= json.load(f)
    return jsonify(error = None, message = "All Objects Are Displayed", data = user_data['data'])

@app.route(f"{base_url}/people/<int:t>")
def specific_id(t):
    with open (data_path, 'r') as f:
        user_data= json.load(f)
    return jsonify(
        error=None,
        message=f"Object with ID {t} is displayed",
        data=user_data['data'][t - 1],
    )

# POST
@app.route(f"{base_url}/people", methods = ["POST","GET"])
def test():
    if request.method == "GET":
        with open(data_path, 'r') as f:
            user_data = json.load(f)
            #print (user_data)
        return jsonify({"error":None, "message":"Here is the required data", "data":user_data['data']})
    elif request.method == "POST":
        a = request.json

        with open(data_path, 'r') as f: #'r' - shows that the file should be read
            user_data = json.load(f) #json.load - used to deserialize/decode(convert json to py)

        if len(a) == 0:
            return jsonify(error = "present", message = "empty json obj")
        if a in user_data['data']:
            return jsonify(error = "present", message = "duplication") 
        else:
            user_data['data'].append(a) #append - used to add an info in the existing dict


        with open(data_path,'w') as f:
            json.dump(user_data,f) #json.dump- used to serialize/encode(converting py to json)
#json.dump is used to write data to a file.| json.dumps() is used to write to a python string
# dump-converts dict of python to obj in json file.| dumps-converts dict obj of py to json string format
        return jsonify(error=None, message = "received sucesully")
        # return (user_data['data'])
# PUT 
@app.route(f"{base_url}/people/data/<int:i>", methods = ["PUT" , "GET","DELETE"])
def user(i):
    if request.method == "DELETE":
        with open(data_path , 'r') as f:
            user_data = json.load(f)

        user_data['data'].pop(i-1)

        with open(data_path,'w') as f:
            json.dump(user_data,f)
        return jsonify(error = None, message=f"Obj with ID {i} is DELETED")
    elif request.method == "GET":
        with open(data_path , 'r') as f:
            user_data = json.load(f)
        return jsonify({"error":None, "message":"Here is the required data", "data":user_data['data']})
    elif request.method == "PUT":
        request_data = request.json

        with open(data_path , 'r') as f:
            user_data = json.load(f)

        user_data['data'][i-1].update(request_data)

        with open(data_path,'w') as f:
            json.dump(user_data,f)
        return jsonify(error = None, message = "Latest Obj Updated")

@app.route(f"{base_url}/people/count")
def count():
    with open(data_path, 'r') as f:
        user_data = json.load(f)
    return jsonify(error = None, message = "The count of objects is %d" % len(user_data['data']))

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 3000)
    