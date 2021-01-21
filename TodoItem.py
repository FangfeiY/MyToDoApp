from TodoDb import db

class TodoItem(db.Model):
    __tablename__ = 'todo_item'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# No longer using SQLAlchemy to manage db tables
# Replaced by using Flask-Migrate to do the work
# Run "flask db migrate"
#db.create_all()




