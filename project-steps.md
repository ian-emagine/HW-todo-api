# FlaskApp1

Flask app created in Windows 10 environment on Visual Studio Code using Powershell terminal.

Original location is user directors of Windows user

Installed pip
```
python -m pip install --upgrade pip
```

Created new environment
```
python -m venv myenv
```

Installed then upgraded Flask
```
pip install flask
pip install flask --upgrade flask
```

Made then entered new project directory
```
md todo_service_flask
cd todo_service_flask
```

Install SQL Lite DB and create a database called todo.db inside the project directory.

Execute the following SQL to create the 
```
CREATE TABLE "items" (
    "item" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    PRIMARY KEY("item")
);
```

Created main.py
```
New-item main.py -ItemType file
```

Added code to main.py which contains all the paths and functions executed when these paths are accessed. I included the import of "helper" script which will be created next. 
```
import helper
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Add item to the list
    res_data = helper.add_to_list(item)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/items/all')
def get_all_items():
    # Get items from the helper
    res_data = helper.get_all_items()

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    return response

@app.route('/item/status', methods=['GET'])
def get_item():
    # Get parameter from the URL
    item_name = request.args.get('name')

    # Get items from the helper
    status = helper.get_item(item_name)

    # Return 404 if item not found
    if status is None:
        response = Response("{'error': 'Item Not Found - %s'}"  % item_name, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response

@app.route('/item/update', methods=['PUT'])
def update_status():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']
    status = req_data['status']

    # Update item in the list
    res_data = helper.update_status(item, status)

    # Return error if the status could not be updated
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response

@app.route('/item/remove', methods=['DELETE'])
def delete_item():
    # Get item from the POST body
    req_data = request.get_json()
    item = req_data['item']

    # Delete item from the list
    res_data = helper.delete_item(item)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return response
```

Created helper.py
```
New-item helper.py -ItemType file
```

Added code to helper.py for connecting to the data base and the CRUD operations
```
import sqlite3

DB_PATH = './todo.db'   # Update this path accordingly
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(item):
    try:
        conn = sqlite3.connect(DB_PATH)

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()

        # Keep the initial status as Not Started
        c.execute('insert into items(item, status) values(?,?)', (item, NOTSTARTED))

        # We commit to save the change
        conn.commit()
        return {"item": item, "status": NOTSTARTED}
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select status from items where item='%s'" % item)
        status = c.fetchone()[0]
        return status
    except Exception as e:
        print('Error: ', e)
        return None

def update_status(item, status):
    # Check if the passed status is a valid value
    if (status.lower().strip() == 'not started'):
        status = NOTSTARTED
    elif (status.lower().strip() == 'in progress'):
        status = INPROGRESS
    elif (status.lower().strip() == 'completed'):
        status = COMPLETED
    else:
        print("Invalid Status: " + status)
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set status=? where item=?', (status, item))
        conn.commit()
        return {item: status}
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from items where item=?', (item,))
        conn.commit()
        return {'item': item}
    except Exception as e:
        print('Error: ', e)
        return None
```

Changed location back to to user directors
```
cd ..
```

Activate environment
```
.\myenv\Scripts\Activate.ps1
```

Changed location to project directory
```
cd todo_service_flask
```

Set environemt variable for FLASK_APP
```
$env:FLASK_APP = "main.py"
```

Run Flask
```
flask run
```

Opened new terminal then ran curl on the root path (/) to ensure server was running
```
curl.exe -X POST http://127.0.0.1:5000/
```

Then ran the path to add a new item using curl
```
curl.exe -X POST http://127.0.0.1:5000/item/new -d '{\"item\": \"Setting up Flask\"}' -H "Content-Type: application/json"
```
*The escaping of the double quotes is important in Windows. It will cause an error otherwise.*

This returned the expected response
```
{"item": "Setting up Flask", "status": "Not Started"}
```

I then added another item to the database
```
curl.exe -X POST http://127.0.0.1:5000/item/new -d '{\"item\": \"Implement POST endpoint\"}' -H "Content-Type: application/json"
```

This returned the expected response
```
{"Implement POST endpoint": "Not Started"}
```

I then ran the URL for viewing all the items in the database:
```
curl.exe -X GET http://127.0.0.1:5000/items/all
```

This returned a dictionary with the number of items and a embedded list with the actual items
```
{"count": 2, "items": [["Setting up Flask", "Not Started"], [Implement POST endpoint", "Not Started"]]}
```

I then ran the URL for getting the status of an individual item. Plus signs (+) had to be used to replace spaces in the item name.
```
curl.exe -X GET http://127.0.0.1:5000/item/status?name=Setting+up+Flask
```

This returned the status of the selected item, "Setting up Flask"
```
{"status": "Not Started"}
```

I then ran the URL for updating the status of an item
```
curl.exe -X PUT http://127.0.0.1:5000/item/update -d '{\"item\": \"Setting up Flask\", \"status\": \"Completed\"}' -H "Content-Type: application/json"
```

It returned the updated item
```
{"Setting up Flask": "Completed"}
```

I then ran the URL for deleting an item
```
curl.exe -X DELETE http://127.0.0.1:5000/item/remove -d '{\"item\": \"Setting up Flask\"}' -H "Content-Type: application/json
```

It returned the confirmation message which is the item that was deleted.
```
{"item": "Setting up Flask"}
```

I then ran the URL for displaying all the items in the database to confirm that the item was removed.
```
curl.exe -X GET http://127.0.0.1:5000/items/all
```

It returned the list of items which now only contained one item.
```
{"count": 1, "items": [["Implement POST Endpoint", "Not Started"]]}
```

I then ran added a function to helper.py to search the list for item names containing a keyword
```
def search_items(keyword):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where item like ?", ('%'+keyword+'%',))
        rows = c.fetchall()
        return { "count": len(rows), "items": rows }
    except Exception as e:
        print('Error: ', e)
        return None
```

I then created the corresponding function and route (/items/search) in main.py
```
@app.route('/items/search', methods=['GET'])
def search_items():
    # Get parameter from the URL
    keyword = request.args.get('keyword')

    # Get items from the helper
    status = helper.search_items(keyword)

    # Return 404 if error performing search
    if status is None:
        response = Response("{'error': 'Error performing search - %s'}"  % keyword, status=404 , mimetype='application/json')
        return response

    # Return status
    res_data = {
        'status': status
    }

    response = Response(json.dumps(res_data), status=200, mimetype='application/json')
    return response
```

I then ran the URL to search for an item matching the keyword "end"
```
curl.exe -X GET http://127.0.0.1:5000/items/search?keyword=end
```

It returned the item in the list that contained the keyword in the name
```
{"status": {"count": 1, "items": [["Implement POST Endpoint", "Not Started"]]}}
```

I then ran the URL to add another item with "end" in the name
```
curl.exe -X POST http://127.0.0.1:5000/item/new -d '{\"item\": \"Implement another POST Endpoint\"}' -H "Content-Type: applictem/newation/json"
```

It returned the details of the newly added item
```
{"item": "Implement another POST Endpoint", "status": "Not Started"}
```

Then I ran the URL to search for items with "end" the name again
```
curl.exe -X GET http://127.0.0.1:5000/items/search?keyword=end
```

This time it returned both items in the list
```
{"status": {"count": 2, "items": [["Implement POST Endpoint", "Not Started"], ["Implement anment another POST Endpoint", "Not Started"]]}}
```


I then decided to put a front end on the app with Jigna templates. I only wanted to be able to do basic CRUD operations from a web interface. The following changes were made to the application.

I added additional required functions from the Flask package within "main.py"
```
from flask import Flask, request, Response, render_template, redirect
```

I created a "templates" folder and inside this folder I placed these files
```
base.html
index.html
add.html
```

base.html contained:
```
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<title>{{ the_title }}</title>

	<!-- note the special href for files in the Flask "static" folder -->
	<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">

</head>
<body>

<div id="container">

  <!-- Jinja directives: page contents will go between them -->
  {% block content %}
  {% endblock %}

</div>

</body>
</html>
```

index.html contained:
```
{% extends 'base.html' %}

{% block content %}

<h1>To Do List</h1>

<p>Click an item to edit it's status</p>
<p><a href="{{ url_for( 'add_form' ) }}"><button>ADD NEW ITEM</button></a></p>
<!-- pairs is a list that must be sent here by a route function
     The list will contain 45 pairs: a presidency number, and a
     president's name -->

    <ul>
    {% for item in result['items'] %}
        <li>{{ item[0] }} ({{ item[1] }}): <a href="{{ url_for( 'update_status', item=item[0], status='in progress' ) }}">Start</a> | <a href="{{ url_for( 'update_status', item=item[0], status='completed' ) }}">Completed</a> | <a href="{{ url_for( 'delete_item', item=item[0] ) }}">Delete</a></li>
    {% endfor %}
    </ul>

{% endblock %}
```

add.html contained:
```
{% extends 'base.html' %}

{% block content %}

<h1>Add Item</h1>

<p>Click an item to edit it's status</p>
<form method="POST" action="{{ url_for( 'add_item' ) }}">
    <label for="item">Item name<input type="text" name="item"></label>
    <input type="submit" name="Submit">
</form>
{% endblock %}
```

I created a folder called "static" and inside this folder I created the "CSS" folder. Inside this folder I added the "main.css" file containgn the following style rules:
```
html {
    font-size: 100%;
    box-sizing: border-box;
}
*, *:before, *:after {
    box-sizing: inherit;
}
body {
    font-family: 'Verdana', sans-serif;
    color: #333;
    background: #238989;
    margin: 0;
}
#container {
    margin: 2em auto;
    max-width: 740px;
    padding: 2rem 4rem;
    background: #fff;
    overflow: auto;
}
h1 {
    font-family: 'Georgia', serif;
    font-size: 3rem;
    margin: 0;
    padding: 0.5rem 0;
}
p, li {
    font-size: 1.4rem;
    line-height: 1.5;
}
img {
    display: block;
    margin: auto;
    max-width: 100%;
}
.right {
    float: right;
    margin: 1.5rem 0 1rem 1rem;
    border: 1px solid #333;
}

/* links */

a {
    color: #009;
    text-decoration: none;
}
a:hover {
    color: #0cc;
    text-decoration: underline;
}

/* media queries */

@media (max-width: 800px) {
    body {
        background: #fff;
    }
    #container {
        margin: 0;
        width: 100%;
        padding: 2rem;
    }
    h1 {
        padding: 0 0 0.3rem 0;
    }
    .right {
        float: none;
        margin: 0;
    }
}
```

Then the hello_world function inside main.py was changed as follows:
```
def hello_world():
    # Get items from the helper
    res_data = helper.get_all_items()

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    json_response = response.get_json()
    return render_template('index.html', result=json_response, the_title="To Do List")
```

The add_item function and the corresponding route were changed as follows:
```@app.route('/item/new', methods=['POST'])
def add_item():
    # Get item from the POST body
    # req_data = request.get_json()
    req_data = request.form
    item = req_data['item']

    # Add item to the list
    res_data = helper.add_to_list(item)

    # Return error if item not added
    if res_data is None:
        response = Response("{'error': 'Item not added - " + item + "'}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    return redirect('/')
```

A new function and route was created to display the add.html form:
```
@app.route('/item/add')
def add_form():
    return render_template('add.html', the_title="Add Item to To Do List")
```

The update_status function and corresponding route was changed as follows:
```
# @app.route('/item/update', methods=['PUT'])
@app.route('/item/update', methods=['GET'])
def update_status():
    # Get item from the POST body
    # req_data = request.get_json()
    req_data = request.args
    item = req_data['item']
    status = req_data['status']

    # Update item in the list
    res_data = helper.update_status(item, status)

    # Return error if the status could not be updated
    if res_data is None:
        response = Response("{'error': 'Error updating item - '" + item + ", " + status   +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    # return response
    return redirect('/')
```

The delete_item function and corresponding route was changed as follows:
```
# @app.route('/item/remove', methods=['DELETE'])
@app.route('/item/remove', methods=['GET'])
def delete_item():
    # Get item from the POST body
    # req_data = request.get_json()
    req_data = request.args
    item = req_data['item']

    # Delete item from the list
    res_data = helper.delete_item(item)

    # Return error if the item could not be deleted
    if res_data is None:
        response = Response("{'error': 'Error deleting item - '" + item +  "}", status=400 , mimetype='application/json')
        return response

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')

    # return response
    return redirect('/')
```

Then from in the terminal, I switched to the directory one level up from the project directory and activated the virtual environment. Then I went back into the project directory:
```
.\myenv\Scripts\Activate.ps1
cd .\todo_service_flask\
```

Then I created a "requirements.txt" file from inside the project directory:
```
pip freeze > requirements.txt
```

Application was available to be viewed via webpage at http://127.0.0.1:5000/
