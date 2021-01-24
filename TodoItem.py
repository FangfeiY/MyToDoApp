from TodoDb import db
from TodoList import TodoList

class TodoItem(db.Model):
    __tablename__ = 'todo_item'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# No longer using SQLAlchemy to manage db tables
# Replaced by using Flask-Migrate to do the work
# Run "flask db migrate"
#db.create_all()




