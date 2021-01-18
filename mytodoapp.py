from flask import render_template, request, redirect, url_for, jsonify, abort
import sys
from TodoDb import app,db
from TodoItem import TodoItem

@app.route('/')
def index():
    todo_list = [
        {'description':'To do 1'},
        {'description':'To do 2'},
        {'description':'To do 3'}
    ]
    return render_template('index.html', data=TodoItem.query.all())

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
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    return error

if __name__ == '__main__':
    app.run()
