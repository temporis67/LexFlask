from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/step1', methods=['POST', 'GET'])
def step1():
    if request.method == 'POST':
        result = request.form

        question = result['question']
        print("Frage: %s" % question)

        return render_template("step1.html", result=result)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
