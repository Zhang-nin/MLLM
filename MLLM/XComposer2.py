import torch
from transformers import AutoModel, AutoTokenizer
from get_Prompts import get
import os
torch.set_grad_enabled(False)

def evaluate(arg):
    # init model and tokenizer
    model = AutoModel.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True).cuda().eval()
    tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer2-vl-7b', trust_remote_code=True)

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        for question in prompt_teps:
            text = '<ImageHere>'+question
            with torch.cuda.amp.autocast():
                response, _ = model.chat(tokenizer, query=text, image=image, history=[], do_sample=False)
                ans.append(response)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output


