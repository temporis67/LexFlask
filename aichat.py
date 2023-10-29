import time


#
# SocketIO/JS based Chat with connect to Jarvis LLM
#

class AiChat:
    socketio = None
    my_jarvis = None

    def __init__(self, socketio, jarvis):
        time_start = time.time()
        self.socketio = socketio
        self.my_jarvis = jarvis
        print("Initializing Chat: %s" % time_start)

    # Ask LLM
    def run_question(self, msg):

        if 'question' in msg and msg['question'] != '':
            question = msg['question']
            # print('Message: ' + repr(message) + ' ## ' + question)
            if 'prompt' in msg:
                prompt = msg['prompt']
                context = msg['context']

                answer = self.my_jarvis.ask(socketio=self.socketio, question=question, prompt=prompt, context=context,
                                            callback=self.messageReceived)

            else:
                answer = "Kein Prompt bekommen."
            print('Answer:' + str(answer))

            ## append answer
            msg['message'] = question
            msg['answer'] = answer

            return msg

    # Handle Messaging w. Client
    def messageReceived(self, msg, methods=['GET', 'POST']):
        print('message was received!!!', msg)

    def handle_wait_event(self, msg, methods=['GET', 'POST']):
        print('received Event "still waiting": ' + str(msg))
        time.sleep(1)
        self.socketio.emit('start waiting', msg, )

    def handle_new_question_event(self, msg, methods=['GET', 'POST']):
        print('received Event "new question": ' + str(msg))
        self.socketio.emit('start waiting', {'data': 'before jarvis'})
        answer = self.run_question(msg)
        # print("New Question:: Answer: %s" % repr(answer))
        self.socketio.emit('answer ready', {'data': 'after jarvis'})
        self.socketio.emit('my response', msg, callback=self.messageReceived)

    def handle_my_event_event(self, json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        # print(repr(json))

        message = dict(json)
        if 'message1' in message and message['message'] != '':
            question = message['message']
            # print('Message: ' + repr(message) + ' ## ' + question)
            if 'prompt' in message:
                prompt = message['prompt']
                context = message['context']

                self.socketio.emit('answer ready', {'data': 'before jarvis'})
                answer = self.my_jarvis.ask(socketio=self.socketio, question=question, prompt=prompt,
                                            context=context, callback=self.messageReceived)
                self.socketio.emit('my event', {'data': 'after jarvis'})
                # answer = "Waiting 4 Jarvis"
            else:
                answer = "Kein Prompt bekommen."
            print('Answer:' + str(answer))

            ## append answer
            json['message'] = question
            json['answer'] = answer

        if 'shall_wait' in message:
            self.socketio.emit('wait info', json, callback=self.messageReceived)

        self.socketio.emit('my response', json, callback=self.messageReceived)
        # socketio.emit('my_event', {'data': 'TestMsg'})
