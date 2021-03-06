from flask import render_template, request, redirect, url_for, jsonify, abort
import sys
from TodoDb import app,db
from TodoItem import TodoItem
from TodoList import TodoList

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/todos/create_sync/<list_id>', methods=['POST'])
def create_todo_sync(list_id):
    description = request.form.get('descrip_sync','')

    error = create_todo(description, list_id, {})

    if error:
        abort (500)
    else:
        return redirect(url_for('get_list_todos', list_id=list_id))

@app.route('/todos/create_async', methods=['POST'])
def create_todo_async():
    response_body = {}
    description = request.get_json()['description']
    list_id = request.get_json()['list_id']

    error = create_todo(description, list_id, response_body)
    
    if error:
        abort (500)
    else:
        return jsonify(response_body)

def create_todo(input_descrip, list_id, response_body):
    error = False

    try:
        input_descrip = input_descrip
        todo = TodoItem(description=input_descrip, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        response_body['description'] = todo.description
        response_body['item_id'] = todo.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return error

# Can also use '/todos/<todo_id>/set-completed' and create the function with argument like "def set_completed_todo(todo_id):""
@app.route('/todos/set-completed', methods=['POST'])
def set_completed_todo():
    try:
        todo_id = request.get_json()['todoId']
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = TodoItem.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('get_list_todos', list_id=todo.id))

@app.route('/todos/del_todo/<todo_id>', methods=['DELETE'])
def del_todo(todo_id):
    error = False
    try:
        print('Item to delete: ', todo_id)
        todo = TodoItem.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({ 'success': True })

@app.route('/lists/create_list', methods=['POST'])
def create_list():
    list_name = request.form.get('list_txt_name','')
    error = False
    list_id = 1

    try:
        todo_list = TodoList(name=list_name)
        db.session.add(todo_list)
        db.session.commit()
        list_id = todo_list.id
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort (500)
    else:
        return redirect(url_for('get_list_todos', list_id=list_id))

@app.route('/lists/get_list_todos/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', 
    todos=TodoItem.query.filter_by(list_id=list_id).order_by('id').all(),
    lists=TodoList.query.order_by('id').all(),
    active_list=TodoList.query.get(list_id))

@app.route('/lists/set-completed', methods=['POST'])
def set_completed_list():
    try:
        list_id = request.args.get('listId')
        completed = request.args.get('completed') == 'true'

        todo_list = TodoList.query.get(list_id)
        todo_list.completed = completed

        for todo in todo_list.todos:
            todo.completed = completed
        
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('get_list_todos', list_id=list_id))

@app.route('/lists/del_list/<list_id>', methods=['DELETE'])
def del_list_cascade(list_id):
    error = False
    try:
        print('List to delete: ', list_id)
        todo_list = TodoList.query.get(list_id)
        db.session.delete(todo_list)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({ 'success': True })

if __name__ == '__main__':
    app.run()
