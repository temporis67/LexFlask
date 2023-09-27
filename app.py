from flask import Flask, render_template, request
from flask_socketio import SocketIO
import my_llama

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'

antwort1 = ""
infotext = my_llama.info_text

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
    else:
        question = "Wer lebte in Preußen?"

    print("Frage: %s" % question)
    answer = my_llama.run_step1(question)

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
    answer = my_llama.run_step2(question, context)

    return render_template("step2.html", question=question, answer=answer, answer_old=answer_old, infotext=context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)
