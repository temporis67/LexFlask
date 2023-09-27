from llama_cpp import Llama
from flask import flash

import time
import my_tools

# LLM settings for GPU
n_gpu_layers = 43  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

model_name = "spicyboros-13b-2.2.Q5_K_M.gguf"


# prepare the template we will use when prompting the AI
template2 = """Use the following pieces of information to answer the user's question.
Act if as if you're responding to documentation questions.
Context: {context}
Question: {question}
Answer in german language.
Helpful answer:
"""

template1 = """Use the following pieces of information to answer the user's question.
Act if as if you're responding to documentation questions.
Context:
Question: {question}
Answer in german language.
Helpful answer:
"""


info_text = """
Es folgt eine Aufzählung der preußischen Könige mit ihren Geburtstagen und Sterbedaten:
Friedrich I. wurde am 11. Juli 1657 geboren und verstarb am 25. Februar 1713.
Friedrich Wilhelm I. wurde am 14. August 1688 geboren und verstarb am 31. Mai 1740.
Friedrich II. wurde am 24. Januar 1712 geboren und verstarb am 17. August 1786.
Friedrich Wilhelm II. wurde am 25. September 1744 geboren und verstarb am 16. November 1797.
Friedrich Wilhelm III. wurde am 3. August 1770 geboren und verstarb am 7. Juni 1840.
Friedrich Wilhelm IV. wurde am 15. Oktober 1795 geboren und verstarb am 2. Januar 1861.
Wilhelm I. wurde am 22. März 1797 geboren und verstarb am 9. März 1888.
Friedrich III. wurde am 18. Oktober 1831 geboren und verstarb am 15. Juni 1888.
Wilhelm II. wurde am 27. Januar 1859 geboren und verstarb am 4. Juni 1941.
Werner von Alvensleben wurde am 20.7.1840 geboren und verstarb am 19.2.1929.
"""
def run_step(prompt):

    time_start = time.time()
    print("Prompt: %s" % prompt)

    flash("Loading model: %s" % model_name)
    # load the large language model file
    LLM = Llama(model_path="/main/PyCharm-Projects/lexbolo/models/gguf/" + model_name,
                n_ctx=2048,
                n_gpu_layers=n_gpu_layers,
                n_batch=n_batch)
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

    time_query= time.time() - time_start - time_to_load
    print("Query executed in %s seconds" % time_query)

    # display the response
    answer = output["choices"][0]["text"]

    time_elapsed = time.time() - time_start
    print(answer)
    flash(f'{model_name} response time: {time_elapsed:.02f} sec')

    return answer


def run_step1(question):
    prompt = template1.format(question=question)
    return run_step(prompt)

def run_step2(question, context):
    prompt = template2.format(question=question, context=context)
    return run_step(prompt)

#
# my_tools.log_benchmark(model_name, prompt, time_elapsed, result)
