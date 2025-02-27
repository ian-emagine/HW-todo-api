import helper
from flask import Flask, request, Response, render_template, redirect
import json
# from modules import convert_to_dict, make_ordinal

app = Flask(__name__)
application = app

@app.route('/')
def hello_world():
    # Get items from the helper
    res_data = helper.get_all_items()

    # Return response
    response = Response(json.dumps(res_data), mimetype='application/json')
    json_response = response.get_json()
    return render_template('index.html', result=json_response, the_title="To Do List")

@app.route('/item/new', methods=['POST'])
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

@app.route('/item/add')
def add_form():
    return render_template('add.html', the_title="Add Item to To Do List")

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