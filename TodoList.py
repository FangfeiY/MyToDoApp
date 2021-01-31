from TodoDb import db

class TodoList(db.Model):
    __tablename__ = 'todo_list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship('TodoItem', backref='parent_list', lazy=True)

    def __repr__(self):
        return f'<Todo list {self.id} {self.name}>'