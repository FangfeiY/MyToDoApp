from flask import render_template, request, redirect, url_for, jsonify, abort
import sys
from TodoDb import app,db
from TodoItem import TodoItem

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))
    

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html', data=TodoItem.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/todos/create_sync', methods=['POST'])
def create_todo_sync():
    error = create_todo(request.form.get('descrip_sync',''), {})

    if error:
        abort (500)
    else:
        return redirect(url_for('index'))

@app.route('/todos/create_async', methods=['POST'])
def create_todo_async():
    response_body = {}
    
    error = create_todo(request.get_json()['description'], response_body)
    
    if error:
        abort (500)
    else:
        return jsonify(response_body)

def create_todo(input_descrip, response_body):
    error = False

    try:
        input_descrip = input_descrip
        todo = TodoItem(description=input_descrip)
        db.session.add(todo)
        db.session.commit()
        response_body['description'] = todo.description
        response_body['id'] = todo.id
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
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    error = False
    try:
        print('Item to delete: ', todo_id)
        TodoItem.query.filter_by(id=todo_id).delete()
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

if __name__ == '__main__':
    app.run()
