from flask import Flask , render_template , url_for , request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

#create and intilize database
db = SQLAlchemy(app)
#specify location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

#create table named Todo and it columns
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	created_date = db.Column(db.DateTime)

	# intilize columns
	def __init__(self, content, created_date=None):
		self.content = content
		#current time
		self.created_date = datetime.utcnow()

	#represent object
	def __repr__(self):
		return '<Task %r>' % self.id

#implement / create DB
db.create_all()

#handle the task
@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		# take the task from the input text
		task_content = request.form['content']
		#create object
		new_task = Todo(content=task_content)

		try:
			#inser it to DB
			db.session.add(new_task)
			#to get the id we have to commit
			db.session.commit()
			#back to home page
			return redirect('/')
		except:
			return "there was an issue creating your task"
	else:
		# if not adding any task, view previous task order it by date created
		tasks = Todo.query.order_by(Todo.created_date).all()
		return render_template('index.html', tasks =tasks);

#delete
@app.route('/delete/<int:id>')
def delete(id):
	#if no id display 404 error page
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		#back to home page
		return redirect('/')
	except:
		return 'There was a problem deleting that task'

#update
# '/update/<int:id> because we will send the id from front to backend
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	# if no id display 404 error page
	task_to_update = Todo.query.get_or_404(id)
	if request.method == 'POST':
		task_to_update.content = request.form['content']

		try:
			db.session.commit()
			return redirect('/')

		except:
			return "There was an issue updating your task"

	#view the updated task with allowing for modifications
	else:
		return render_template('update.html',task_to_update=task_to_update )

if __name__ == '__main__':
	app.run(debug=True)