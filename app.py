from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "TodoApp"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class taskList(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  task_data = db.Column(db.String(255), unique=True)

  def __init__ (self, task_data):
    self.task_data = task_data
    

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

      db.session.delete(find)
      db.session.commit()

    else:
      all_task = [db.session.delete(data) for data in taskList.query.all()]
      db.session.commit()

  all_task = taskList.query.all()
  count = taskList.query.count()
  return render_template('index.html', all_task = all_task, count=count)


if __name__ == '__main__':
  app.run(debug=True) 