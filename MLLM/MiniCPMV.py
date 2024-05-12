import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import os
from get_Prompts import get
def evaluate(arg):
    model = AutoModel.from_pretrained('openbmb/MiniCPM-V', trust_remote_code=True, torch_dtype=torch.bfloat16)
    # For Nvidia GPUs support BF16 (like A100, H100, RTX3090)
    # model = model.to(device='cuda', dtype=torch.bfloat32)
    # For Nvidia GPUs do NOT support BF16 (like V100, T4, RTX2080)
    model = model.to(device='cuda', dtype=torch.float16)

    tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-V', trust_remote_code=True)
    model.eval()

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = Image.open(arg.img_path+img).convert('RGB')
        ans = []
        for question in prompt_teps:
            msgs = [{'role': 'user', 'content': question}]
            out, context, _ = model.chat(
                image=image,
                msgs=msgs,
                context=None,
                tokenizer=tokenizer,
                sampling=True,
                temperature=0.7
            )
            ans.append(out)
        res = {"id":img.split(".")[0],"answers":ans}
        output.append(res)
        # with open(img_path[i]+".jsonl","a") as f:
        #     json.dump(res,f)
        #     f.write("\n")
    return output