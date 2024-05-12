import torch
from PIL import Image
from transformers import AutoModelForCausalLM, LlamaTokenizer
from get_Prompts import get
import os


def evaluate(arg):
    tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')  # https://huggingface.co/THUDM/cogvlm-chat-hf
    model = AutoModelForCausalLM.from_pretrained(
        'THUDM/cogvlm-chat-hf',
        torch_dtype=torch.bfloat16,
        low_cpu_mem_usage=True,
        trust_remote_code=True
    ).to('cuda').eval()

    prompt_teps = get(arg.task)
    output = []
    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        for question in prompt_teps:
            image = Image.open(image).convert('RGB')
            inputs = model.build_conversation_input_ids(tokenizer, query=question, history=[], images=[image])
            inputs = {
                'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
                'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
                'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
                'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
            }
            gen_kwargs = {"max_length": 2048, "do_sample": False}
            with torch.no_grad():
                outputs = model.generate(**inputs, **gen_kwargs)
                outputs = outputs[:, inputs['input_ids'].shape[1]:]
                response = tokenizer.decode(outputs[0])
                ans.append(response)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output

