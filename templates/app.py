import re

app = Flask(__name__)

@app.route('/')
def home():
   try:
       return render_template('home.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the home page: " + str(e))

@app.route('/menu')
def menu():
   try:
       return render_template('menu.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the menu page: " + str(e))

@app.route('/clone_training')
def clone_training():
   try:
       return render_template('clone_training.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the clone training page: " + str(e))

@app.route('/database_storage')
def database_storage():
   try:
       return render_template('database_storage.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the database/storage page: " + str(e))

@app.route('/watch_page')
def watch_page():
   try:
       return render_template('watch_page.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the watch page: " + str(e))

@app.route('/banking_api')
def banking_api():
   try:
       return render_template('banking_api.html')
   except Exception as e:
       abort(500, description="Error occurred in rendering the banking API page: " + str(e))

if __name__ == '__main__':
   app.run(debug=False)  # change to False to prevent debug information disclosure.