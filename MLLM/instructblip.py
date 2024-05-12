from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
from get_Prompts import get
import os

def evaluate(task):
    model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b")
    processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    prompt_teps = get()
    output = []
    for img in os.listdir(task):
        image = task + img
        image = Image.open(image)
        ans = []
        for question in prompt_teps:
            inputs = processor(images=image, text=question, return_tensors="pt").to(device)
            outputs = model.generate(
                **inputs,
                do_sample=False,
                num_beams=5,
                max_length=256,
                min_length=1,
                top_p=0.9,
                repetition_penalty=1.5,
                length_penalty=1.0,
                temperature=1,
            )
            generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
            ans.append(generated_text)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output

