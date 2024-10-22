

## IMPORT LIBRARIES ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

#importing the Flask "CLASS"  from the MODULE "flask"  and renaming it as Flask

#importing render_template from the flask module  
# >>>>>> render_template() is a "function" provided by Flask framework, that is used to render an HTML template. 

#  This function takes the name of the HTML file as an argument and renders it as a response to the client's request

# This function is part of Flask's templating system. 
# Flask uses Jinja2 for templating allowing the user to embed python code within the HTML templates.

from flask import Flask,render_template,redirect, request

#for styling the HTML page, using Sass version of CSS
from flask_scss import Scss
# for database, using SQLAlchemy
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime


## DESIGNATING NAME TO THE CLASS OF FLASK ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Here, creating an instance(a specific OBJECT) of the Flask CLASS to initialize the Flask web application
# the instance we created here is named "app_obj",as this is an object of the CLASS "Flask"
#__name__ is used as an argument/ method on the CLASS "Flask" .
#the" __name__ " variable is passed as an argument,to the "Flask" class,when creating the Flask application object "app_obj".

app_obj = Flask(__name__) 
# putting the app as an argument through the CSS module to activate the stylings in the app
Scss(app_obj)

## CONFIGURING SQLALCHEMY DATABASE -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# configuring the SQLalchemy from the configuration under SQLAlchemy site


app_obj.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database_Flask_Tutorial.db"
app_obj.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

# db is an "object" of SQLAlchemy with "app_obj" as an argument

db = SQLAlchemy(app_obj)

#           ## CREATING A MODEL --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# making a class of Mytask, (HOLDING INFORMATION,~ ROW OF DATA), 

class MyTask(db.Model):
    # each item has an unique id, no same task can have the same id
    # thats how we are going to remove and update these items  
    # What is the id - ID is the name of the column in the database table,unique identifier for each record
    # db.Column: This is a method that defines a column in a database table,
    #  >>>>>>>>>>> with argument as "db.Integer" -This specifies the data type for the column and 
    # >>>>>>>>>>> primary_key=True: This indicates that the id column is the primary key for the table

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String (100), nullable=False)
    complete = db.Column(db.Integer,default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Task{self.id}"
    
with app_obj.app_context():
        db.create_all()

## CREATING ROUTE --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#creating route- using a decorater and maps the URL path to a specific function
#the @ symbol is used for decorators in Python. It modifies the behavior of a function
# .route("/") tells Flask to associate the root URL ("/") of the web application with a specific function.

### SENDING & RECIEVING DATA  
#>>>>>>>>>The argument of methods : get and post
# >>>>>>>>>> As there are 2 methods, so a list is created under "method"

@app_obj. route  ("/", methods=['POST','GET'])


## CALLING HOME PAGE -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#  making the first MAin page "index"- the Home page of the application "app_obj"
#def function named "index". in the contest of Flask, this "def" function works as- "view function" / "Route handler"
# what does a view function do?- returns a response when specific URL is accessed.
# Return Render_template : After merging the HTML template and the data you pass in, it generates the final HTML page that can be sent to the client's browser

def index():
    # if the mthod of reuqest is Post, then i am trying to SEND data
    if request.method == 'POST':
        # then i need to gather content
        current_task = request.form['content']
        new_task = MyTask(content=current_task) 
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR:{e}"
        
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)
    
## DELETE AN ITEM
@app_obj.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

## EDIT AN ITEM
@app_obj.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html',task=task)




# ## RUNNER AND DEBUGGER ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# if the name file is executed directly, the value of __name__ will be set to "__main__"
if __name__ == "__main__":
    # app_obj.run(): is a  method that starts the Flask development server.
    # automatically reloading the server if any changes are made to the code, making development smoother.
    # debug=True: enables the Flask debug mode, providing
    # and if an error occurs while running the application, Flask will show detailed error messages (called a traceback) in the browser

    # >>>>>>>>>> app_obj.app_context(): This creates an application context for the Flask app (app_obj). In Flask, certain operations, such as interacting with the database, need to be performed within an "application context" because some objects (like current_app, g, etc.) are tied to the app. The app_context() method ensures that these objects are accessible.
    # >>>>>>>>>>> he with statement is used here to manage the application context. When you enter the with block, the application context is pushed, making it the active context. When the block is exited, the context is popped, meaning it's no longer active, and any associated resources are cleaned up.

    # >>>>>>>>>>> db.create_all(): This command creates all the data ctables based on the models you've defined in your application. It examines the models (which are typically subclasses of db.Model), generates the necessary SQL commands, and creates the tables in the database if they don't already exist.


    

    app_obj.run(debug=True)