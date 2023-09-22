from llama_cpp import Llama

import time
import my_tools

# LLM settings for GPU
n_gpu_layers = 43  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.


# prepare the template we will use when prompting the AI
template = """Use the following pieces of information to answer the user's question.
Act if as if you're responding to documentation questions.
If you don't know the answer exactly, just say so.
Context:
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
Question: Wann lebte König Friedrich Wilhelm der II. von Preußen?
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
"""




# create a text prompt
# prompt = "Q: Wann wurde Friedrich Wilhelm der III. geboren? A: "

prompt = template

model_name = "spicyboros-13b-2.2.Q5_K_M.gguf"


time_start = time.time()

# load the large language model file
LLM = Llama(model_path="models/gguf/" + model_name,
            n_gpu_layers=n_gpu_layers,
            n_batch=n_batch)

# generate a response
output = LLM(prompt,
             max_tokens=256,
             stop=["Q:", "\n"],
             echo=True,
             temperature=0,
             top_p=0,
             top_k=1,
             )

time_elapsed = time.time() - time_start

# display the response
result = output["choices"][0]["text"]

print(result)
print(f'{model_name} response time: {time_elapsed:.02f} sec')

my_tools.log_benchmark(model_name, prompt, time_elapsed, result)
