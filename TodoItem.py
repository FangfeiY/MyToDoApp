from TodoDb import db

class TodoItem(db.Model):
    __tablename__ = 'todo_item'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

# Add some sample data if no data in db
current_items_count = TodoItem.query.count()

if current_items_count == 0:
    for num in range(6):
        item = TodoItem(description=f'To do {num}')
        db.session.add(item)

    db.session.commit()




