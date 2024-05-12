from MLLM.mPLUG.mPLUG_Owl2.mplug_owl2.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from MLLM.mPLUG.mPLUG_Owl2.mplug_owl2.conversation import conv_templates, SeparatorStyle
from MLLM.mPLUG.mPLUG_Owl2.mplug_owl2.model.builder import load_pretrained_model
from MLLM.mPLUG.mPLUG_Owl2.mplug_owl2.mm_utils import process_images, tokenizer_image_token, get_model_name_from_path, KeywordsStoppingCriteria
from transformers import TextStreamer
import torch
from PIL import Image
from get_Prompts import get
import os

def evaluate(arg):
    model_path = 'MAGAer13/mplug-owl2-llama2-7b'
    model_name = get_model_name_from_path(model_path)
    tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, None, model_name,
                                                                           load_8bit=False, load_4bit=False,
                                                                           device="cuda")

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        ans = []
        conv = conv_templates["mplug_owl2"].copy()

        image = Image.open(image).convert('RGB')
        image_tensor = process_images([image], image_processor)
        image_tensor = image_tensor.to(model.device, dtype=torch.float16)

        for question in prompt_teps:
            inp = DEFAULT_IMAGE_TOKEN + question

            conv.append_message(conv.roles[0], inp)
            conv.append_message(conv.roles[1], None)
            prompt = conv.get_prompt()

            input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(
                0).to(model.device)
            stop_str = conv.sep2
            keywords = [stop_str]
            stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
            streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

            temperature = 0.7
            max_new_tokens = 512

            with torch.inference_mode():
                output_ids = model.generate(
                    input_ids,
                    images=image_tensor,
                    do_sample=True,
                    temperature=temperature,
                    max_new_tokens=max_new_tokens,
                    streamer=streamer,
                    use_cache=True,
                    stopping_criteria=[stopping_criteria])

            outputs = tokenizer.decode(output_ids[0, input_ids.shape[1]:]).strip()
            ans.append(outputs)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output