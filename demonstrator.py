from llama_cpp import Llama
import time
from flask_socketio import SocketIO
import asyncio

# LLM settings for GPU
n_gpu_layers = 43  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# model_name = "spicyboros-13b-2.2.Q5_K_M.gguf"
model_name = "Llama-2-13b-chat-german-GGUF.q5_K_M.bin"

# this is the prompt without context
template0 = """
<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, 
explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information. 
Please answer in the same language as the user.

<</SYS>>

{question}[/INST] This is a answer </s>
"""

# this is the prompt with context
template01 = """
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

def run_step(prompt, question, my_llm):
    time_start = time.time()
    print("** Question1: %s" % question)
    print("** Prompt1: ", prompt)

    print("Loading model: %s" % model_name)
    # load the large language model file
    LLM = my_llm
    time_to_load = time.time() - time_start
    print("loaded model %s in %s seconds" % (model_name, time_to_load))

    # generate a response
    output = LLM(prompt,
                 max_tokens=256,
                 stop=["Q:", "\n"],
                 echo=False,
                 temperature=0,
                 top_p=0,
                 top_k=1,
                 )

    time_query = time.time() - time_start - time_to_load
    print("Query executed in %s seconds" % time_query)

    # display the response
    answer = output["choices"][0]["text"]

    time_elapsed = time.time() - time_start
    print("  Frage: %s" % question)
    print("Antwort: %s" % answer)
    print(f'{model_name} response time: {time_elapsed:.02f} sec')

    if answer.strip() == "" or str(answer).strip() == str(question).strip():
        print("Empty answer.")
        answer = "Das weiß ich leider nicht."

    return answer


def run_step1(question, llm):
    prompt = template0.format(question=question)
    return run_step(prompt, question, llm)


def run_step2(question, context, llm):
    prompt = template01.format(question=question, context=context)
    return run_step(prompt, question, llm)
