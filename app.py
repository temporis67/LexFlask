from flask import Flask, render_template, request
import demonstrator
from flask_socketio import SocketIO
from jarvis import Jarvis
from aichat import AiChat


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

socketio = SocketIO(app)

my_jarvis = Jarvis()
my_chat = AiChat(socketio=socketio, jarvis=my_jarvis)


#
# Static Pages
#
@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


#
# Hook for SocketIO Chat App AiChat
#
@app.route('/chat', methods=['POST', 'GET'])
def chat():
    return render_template('chat.html')


@socketio.on('my event')
def handle_my_event_event(json, methods=['GET', 'POST']):
    my_chat.handle_my_event_event(json)

@socketio.on('new question')
def handle_new_question_event(msg, methods=['GET', 'POST']):
    my_chat.handle_new_question_event(msg)

@socketio.on('still waiting')
def handle_wait_event(msg, methods=['GET', 'POST']):
    my_chat.handle_wait_event(msg)
#
# pages for classic demonstrator
#

@app.route('/step1', methods=['POST', 'GET'])
def step1():
    if request.method == 'POST':
        result = request.form
        question = result['question']
    else:
        question = "Wer lebte in Preußen?"

    print("Frage: %s" % question)
    answer = demonstrator.run_step1(question, my_jarvis.llm)

    return render_template("step1.html", question=question, answer=answer)


@app.route('/step2', methods=['POST', 'GET'])
def step2():
    if request.method == 'POST':
        result = request.form

        question = result['question']
        context = result['context']
        answer_old = result['answer_old']
    else:
        question = "Wer lebte in Preußen?"
        context = "In Preußen lebten die Preußen."
        answer_old = "Unsinn"

    print("Frage: %s" % question)
    answer = demonstrator.run_step2(question, context, my_jarvis.llm)

    return render_template("step2.html", question=question, answer=answer, answer_old=answer_old, infotext=context)


#
# Start SocketIO App
#
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port="80", debug=False)
