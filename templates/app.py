import re

app = Flask(__name__)

def render_template_with_error_handling(template_name):
    try:
        return render_template(template_name)
    except Exception as e:
        abort(500, description="Error occurred in rendering the {} page: ".format(template_name) + str(e))

@app.route('/')
def home():
   return render_template_with_error_handling('home.html')

@app.route('/menu')
def menu():
   return render_template_with_error_handling('menu.html')

@app.route('/clone_training')
def clone_training():
   return render_template_with_error_handling('clone_training.html')

@app.route('/database_storage')
def database_storage():
   return render_template_with_error_handling('database_storage.html')

@app.route('/watch_page')
def watch_page():
   return render_template_with_error_handling('watch_page.html')

@app.route('/banking_api')
def banking_api():
   return render_template_with_error_handling('banking_api.html')

if __name__ == '__main__':
   app.run(debug=False)  # change to False to prevent debug information disclosure.