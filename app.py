from flask import Flask, render_template, request
import my_llama
from flask_socketio import SocketIO
from jarvis import Jarvis
from llama_cpp import Llama
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

socketio = SocketIO(app)

antwort1 = ""
infotext = my_llama.info_text

my_jarvis = None

my_jarvis = Jarvis()


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/chat',  methods=['POST', 'GET'])
def chat():
    return render_template('chat.html')

@app.route('/debug',  methods=['POST', 'GET'])
def debug():
    if request.method == 'POST':
        result = request.form
        question = result['question']
    else:
        question = "Wer lebte in Preußen?"

    prompt2 = """
    <s>[INST]<<SYS>>Du bist ein freundlicher Assistent.
    Benutze die folgenden Informationen, um die Frage des Nutzers zu beantworten.
    {context}
    <</SYS>>{question}[/INST] This is a answer </s>
    {question}"""

    context2 = "In Preußen lebten viele fleißige Handwerker, wie zum Beispiel Bäcker, Schmiede und Schuster."
    prompt = """
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, 
explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information but answer with "I don't know.". 
Please answer in the same language as the user. Please answer in full sentences.

Use the following pieces of information to answer the user's question:
{context}
<</SYS>>

{question}[/INST] This is a answer </s>
"""
    context = "Hamburg liegt in der Nähe von Bremen. Beide sind ehemalige Hanse-Städte."
    answer2 = "OFF"


    print("Frage: %s" % question)
    if(my_jarvis.llm != None):
        answer = my_jarvis.ask(socketio=socketio, question=question, prompt=prompt, context=context, callback=messageReceived)
        print("First run finished...", answer2)
        # answer = my_llama.run_step1(question, my_jarvis.llm)

    else:
        answer = "LLM is off (debug)"

    print("Antwort 1:", answer)
    # print("Antwort 2:", answer2)

    return render_template("debug.html", question=question, answer=answer, answer2=answer2)


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



def messageReceived(msg, methods=['GET', 'POST']):
    print('message was received!!!', msg)

@socketio.on('still waiting')
def handle_wait_event(msg, methods=['GET', 'POST']):
    print('received Event "still waiting": ' + str(msg))
    time.sleep(1)
    socketio.emit('start waiting', msg,)

## just seperating the content habdling from event
def run_question(msg):

    if 'question' in msg and msg['question'] != '':
        question = msg['question']
        # print('Message: ' + repr(message) + ' ## ' + question)
        if 'prompt' in msg:
            prompt = msg['prompt']
            context = msg['context']

            answer = my_jarvis.ask(socketio=socketio, question=question, prompt=prompt,
                                   context=context, callback=messageReceived)

        else:
            answer = "Kein Prompt bekommen."
        print('Answer:' + str(answer))

        ## append answer
        msg['message'] = question
        msg['answer'] = answer

        return msg


@socketio.on('new question')
def handle_new_question_event(msg, methods=['GET', 'POST']):
    print('received Event "new question": ' + str(msg))
    socketio.emit('start waiting', {'data': 'before jarvis'})
    answer = run_question(msg)
    print("New Question:: Answer: %s" % repr(answer))
    socketio.emit('answer ready', {'data': 'after jarvis'})
    socketio.emit('my response', msg, callback=messageReceived)


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    # print(repr(json))

    message = dict(json)
    if 'message1' in message and message['message'] != '':
        question = message['message']
        # print('Message: ' + repr(message) + ' ## ' + question)
        if 'prompt' in message:
            prompt = message['prompt']
            context = message['context']
            ## ask question my_llama
            print("HERE")
            socketio.emit('answer ready', {'data': 'before jarvis'})
            answer = my_jarvis.ask(socketio=socketio, question=question, prompt=prompt,
                                   context=context, callback=messageReceived)
            socketio.emit('my event', {'data': 'after jarvis'})
            # answer = "Waiting 4 Jarvis"
        else:
            answer = "Kein Prompt bekommen."
        print('Answer:' + str(answer))

        ## append answer
        json['message'] = question
        json['answer'] = answer

    if 'shall_wait' in message:
        socketio.emit('wait info', json, callback=messageReceived)

    socketio.emit('my response', json, callback=messageReceived)
    # socketio.emit('my_event', {'data': 'TestMsg'})

if __name__ == '__main__':
    socketio.run(app, debug=True)




# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port="80", debug=False)
