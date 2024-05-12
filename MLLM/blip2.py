from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
from get_Prompts import get
import os
def evaluate(arg):

    device = "cuda" if torch.cuda.is_available() else "cpu"

    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained( "Salesforce/blip2-opt-2.7b", torch_dtype=torch.float16)
    model.to(device)

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        for question in prompt_teps:
            image = [Image.open(image)]
            inputs = processor(images=image, text=question, return_tensors="pt").to(device, torch.float16)
            generated_ids = model.generate(**inputs)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            ans.append(generated_text)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output
