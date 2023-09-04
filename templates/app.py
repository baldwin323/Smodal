from flask import Flask, render_template, abort
import re

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering the home page: " + str(e))

@app.route('/page1')
def page1():
    try:
        return render_template('page1.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering page 1: " + str(e))

@app.route('/page2')
def page2():
    try:
        return render_template('page2.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering page 2: " + str(e))

@app.route('/page3')
def page3():
    try:
        return render_template('page3.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering page 3: " + str(e))    

@app.route('/page4')
def page4():
    try:
        return render_template('page4.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering page 4: " + str(e)) 
    
@app.route('/page5')
def page5():
    try:
        return render_template('page5.html')
    except Exception as e:
        abort(500, description="Error occurred in rendering page 5: " + str(e))     

@app.route('/page_count')
def page_count():
    # Enhanced input validation to check if pages are integers
    def validate(value):
        if not re.match(r"^[0-9]*$", value):
            raise ValueError("Invalid input: " + value)
    
    try:
        validate('page1')
        validate('page2')
        validate('page3')
        validate('page4')
        validate('page5')

        is_page1_complete = render_template('page1.html') is not None
        is_page2_complete = render_template('page2.html') is not None
        is_page3_complete = render_template('page3.html') is not None
        is_page4_complete = render_template('page4.html') is not None
        is_page5_complete = render_template('page5.html') is not None
        page_count = sum([is_page1_complete, is_page2_complete, is_page3_complete, is_page4_complete, is_page5_complete])
        
        return "The number of completed pages is: "+str(page_count)
    
    except ValueError as v:
        abort(500, description="Invalid input: " + str(v))
    
    except Exception as e:
        abort(500, description="Error occurred in getting page count: " + str(e))

if __name__ == '__main__':
    app.run(debug=False)  # change to False to prevent debug information disclosure.