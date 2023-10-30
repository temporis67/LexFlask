from llama_cpp import Llama
import time

# LLM settings for GPU
n_gpu_layers = 43  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# model_name = "spicyboros-13b-2.2.Q5_K_M.gguf"
model_name = "Llama-2-13b-chat-german-GGUF.q5_K_M.bin"
LOAD_LLM = "ON"


class Jarvis:
    llm = None

    def ask(self, socketio, question, prompt, context, callback):
        time_start = time.time()

        if prompt != "":
            prompt2 = prompt.format(question=question, context=context)
        else:
            prompt2 = question

        # print("start jarvis.ask(): %s" % question)

        if LOAD_LLM != "OFF":
            output = self.llm(prompt2,
                              max_tokens=256,
                              stop=["Q:", "\n"],
                              echo=False,
                              temperature=0,
                              top_p=0,
                              top_k=1,
                              )
            # print("** Answer ready ask(): ", repr(output))

        else:
            # print('Warning: LOAD_LLM == "OFF"')
            time.sleep(2)
            # print('Ende jarvis.ask()')
            return "Das LLama Modell ist deaktiviert."

        time_query = time.time() - time_start
        print("Query executed in %s seconds" % time_query)

        answer = output["choices"][0]["text"]

        return answer

    def __init__(self):
        time_start = time.time()
        print("Loading model: %s" % model_name)
        # load the large language model file
        if (LOAD_LLM != "OFF"):
            self.llm = Llama(model_path="models/" + model_name,
                             n_ctx=2048,
                             n_gpu_layers=n_gpu_layers,
                             n_batch=n_batch,
                             verbose=True)
        else:
            self.llm = None

        time_to_load = time.time() - time_start
        print("loaded model %s in %s seconds" % (model_name, time_to_load))
