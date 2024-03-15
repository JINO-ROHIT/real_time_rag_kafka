from kafka import KafkaConsumer
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, TextIteratorStreamer

from vlite_db.main import VLite
from vlite_db.utils import *

import warnings
warnings.simplefilter("ignore")

system_prompt = """[INST] <<SYS>>
You are a helpful python assistant. Given the context , answer the user's query ONLY with the current context. DONOT make up anything and if you dont know the answer, just say you dont know.
<</SYS>>
"""

db = VLite('vlite_20240315_191416.npz')
consumer = KafkaConsumer('myfirsttopic', bootstrap_servers='localhost:9092')

def load():
    model_name_or_path = r'E:\huggingface\hub\models--meta-llama--Llama-2-7b-chat-hf\snapshots\c1b0db933684edbfe29a06fa47eb19cc48025e93'

    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,
                                            use_fast=True)
    streamer = TextIteratorStreamer(tokenizer)

    model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
            trust_remote_code=True,
            device_map = "cuda:0",
            load_in_4bit = True
    )
        
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=0.1,
        top_p=0.95,
        repetition_penalty=1.15,
        )
    
    return tokenizer, streamer, model, pipe

tokenizer, streamer, model, pipe = load()

def generate(input, max_new_tokens):
    response = pipe(input, max_new_tokens=max_new_tokens)[0]['generated_text']
    return response

while True:
    for message in consumer:
        user_query = message.value.decode()

        extracted_chunks, _ = db.remember(user_query, top_k = 3)

        context = ""
        for _text in extracted_chunks:
            context += _text
            
        message = system_prompt + "\n\n USER QUERY \n" + user_query + "\n\n CONTEXT: \n" + context
        message += ' [/INST]'

        #print(message)

        final_response = generate(message, max_new_tokens = 512)
        print(final_response.split("[/INST]")[-1].strip().split(':')[-1].strip())