from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page_count')
def page_count():
    # Checks if the pages are completed and returns the count
    is_page1_complete = render_template('page1.html') is not None
    is_page2_complete = render_template('page2.html') is not None
    page_count = sum([is_page1_complete, is_page2_complete])
    return "The number of completed pages is: "+str(page_count)

if __name__ == '__main__':
    app.run(debug=True)