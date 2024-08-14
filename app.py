from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "TodoApp"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class taskList(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  task_data = db.Column(db.String(50), unique=True)
  status = db.Column(db.Integer)

  def __init__ (self, task_data):
    self.task_data = task_data
    self.status = 0
    

@app.route('/', methods = ["GET",'POST'])
def home():

  if request.method == 'POST':

    response = request.form['action']

    if response == "add":

      data = request.form['task']
      find = taskList.query.filter_by(task_data=data).first()
      if not find:
        db.session.add(taskList(data))
        db.session.commit()
    
    elif response == 'delete':

      data = request.form['task']

      find = taskList.query.filter_by(id=data).first()

      if find:
        db.session.delete(find)
        db.session.commit()

    elif response == 'markdown':

      data = request.form['task']

      find = taskList.query.filter_by(id=data).first()
      find.status = 1
      db.session.commit()

    elif response == 'close_markdown':

      data = request.form['task']

      find = taskList.query.filter_by(id=data).first()
      find.status = 0
      db.session.commit()

    else:

      all_task = [db.session.delete(data) for data in taskList.query.all()]
      db.session.commit()
    
    

  all_task = taskList.query.all()
  count = taskList.query.count()
  return render_template('index.html', all_task = all_task, count=count)


if __name__ == '__main__':

  app.run(debug=True) 