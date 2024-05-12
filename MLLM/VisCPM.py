from MLLM.viscpm.VisCPM import VisCPMChat
from PIL import Image
from get_Prompts import get
import os

def evaluate(arg):
    model_path = "/path/to/checkpoint"
    viscpm_chat = VisCPMChat(model_path, image_safety_checker=True)

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        image = Image.open(image).convert("RGB")
        for question in prompt_teps:
            answer, _, _ = viscpm_chat.chat(image, question)
            ans.append(answer)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output
