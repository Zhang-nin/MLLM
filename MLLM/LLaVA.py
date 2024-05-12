from MLLM.llava.llava.mm_utils import get_model_name_from_path
from MLLM.llava.llava.eval.run_llava import eval_model
from get_Prompts import get
import os

def evaluate(arg):
    model_path = "liuhaotian/llava-v1.5-7b"

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        for question in prompt_teps:
            args = type('Args', (), {
                "model_path": model_path,
                "model_base": None,
                "model_name": get_model_name_from_path(model_path),
                "query": question,
                "conv_mode": None,
                "image_file": image,
                "sep": ",",
                "temperature": 0,
                "top_p": None,
                "num_beams": 1,
                "max_new_tokens": 512
            })()
            response = eval_model(args)
            ans.append(response)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output
