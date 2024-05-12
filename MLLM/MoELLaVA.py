import torch
from PIL import Image
from MLLM.moellava.moellava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from MLLM.moellava.moellava.conversation import conv_templates, SeparatorStyle
from MLLM.moellava.moellava.model.builder import load_pretrained_model
from MLLM.moellava.moellava.utils import disable_torch_init
from MLLM.moellava.moellava.mm_utils import tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from get_Prompts import get
import os

def evaluate(arg):
    disable_torch_init()
    model_path = 'LanguageBind/MoE-llava-Phi2-2.7B-4e'  # LanguageBind/MoE-llava-Qwen-1.8B-4e or LanguageBind/MoE-llava-StableLM-1.6B-4e
    device = 'cuda'
    load_4bit, load_8bit = False, False  # FIXME: Deepspeed support 4bit or 8bit?
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, processor, context_len = load_pretrained_model(model_path, None, model_name, load_8bit, load_4bit, device=device)
    image_processor = processor['image']
    conv_mode = "phi"  # qwen or stablelm
    conv = conv_templates[conv_mode].copy()


    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image_tensor = image_processor.preprocess(Image.open(arg.img_path+img).convert('RGB'), return_tensors='pt')[
            'pixel_values'].to(model.device, dtype=torch.float16)
        ans = []
        for question in prompt_teps:

            inp = DEFAULT_IMAGE_TOKEN + '\n' + question

            conv.append_message(conv.roles[0], inp)
            conv.append_message(conv.roles[1], None)
            prompt = conv.get_prompt()
            input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
            stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
            keywords = [stop_str]
            stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

            with torch.inference_mode():
                output_ids = model.generate(
                    input_ids,
                    images=image_tensor,
                    do_sample=True,
                    temperature=0.2,
                    max_new_tokens=1024,
                    use_cache=True,
                    stopping_criteria=[stopping_criteria])

            outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:], skip_special_tokens=True).strip()
            ans.append(outputs)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output
