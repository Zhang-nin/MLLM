from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
from get_Prompts import get
import os

def evaluate(arg):
    torch.manual_seed(1234)
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        for question in prompt_teps:
            response, history = model.chat(tokenizer, query=f'<img>{image}</img>'+prompt, history=None)
            ans.append(response)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output