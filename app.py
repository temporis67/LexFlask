from flask import Flask, render_template, request
import my_llama
from flask_socketio import SocketIO
from my_llama import Jarvis
from llama_cpp import Llama

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

socketio = SocketIO(app)

antwort1 = ""
infotext = my_llama.info_text

my_jarvis = Jarvis()

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/chat',  methods=['POST', 'GET'])
def chat():
    return render_template('chat.html')


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/step1', methods=['POST', 'GET'])
def step1():
    if request.method == 'POST':
        result = request.form
        question = result['question']
    else:
        question = "Wer lebte in Preußen?"

    print("Frage: %s" % question)
    answer = my_llama.run_step1(question,my_jarvis.llm)

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
    answer = my_llama.run_step2(question, context, my_jarvis.llm)

    return render_template("step2.html", question=question, answer=answer, answer_old=answer_old, infotext=context)



## for chat


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))

    message = dict(json)
    if 'message' in message and message['message'] is not '':
        question =  message['message']
        # print('Message: ' + repr(message) + ' ## ' + question)
        if 'prompt' in message:
            prompt = message['prompt']
            context = message['context']
            ## ask question my_llama
            answer = my_jarvis.ask(question, prompt, context)
        else:
            answer = "Kein Prompt bekommen."
        print('Answer:' + answer)

        ## append answer
        json['message'] = question
        json['answer'] = answer


    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=False)


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port="80", debug=False)
