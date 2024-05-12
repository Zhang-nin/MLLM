from MLLM.mPLUG.mPLUG_Owl.mplug_owl.modeling_mplug_owl import MplugOwlForConditionalGeneration
from MLLM.mPLUG.mPLUG_Owl.mplug_owl.tokenization_mplug_owl import MplugOwlTokenizer
from MLLM.mPLUG.mPLUG_Owl.mplug_owl.processing_mplug_owl import MplugOwlImageProcessor, MplugOwlProcessor
import torch
from PIL import Image
from get_Prompts import get
import os

def evaluate(arg):
    pretrained_ckpt = 'MAGAer13/mplug-owl-llama-7b'
    model = MplugOwlForConditionalGeneration.from_pretrained(pretrained_ckpt, torch_dtype=torch.bfloat16, )
    image_processor = MplugOwlImageProcessor.from_pretrained(pretrained_ckpt)
    tokenizer = MplugOwlTokenizer.from_pretrained(pretrained_ckpt)
    processor = MplugOwlProcessor(image_processor, tokenizer)

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):
        image = arg.img_path + img
        images = [Image.open(image)]
        ans = []
        for question in prompt_teps:
            prompts = [
                '''The following is a conversation between a curious human and AI assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
            Human: <image>
            Human: {}.
            AI: '''.format(question)]
            generate_kwargs = {'do_sample': True, 'top_k': 5, 'max_length': 512}
            inputs = processor(text=prompts, images=images, return_tensors='pt')
            inputs = {k: v.bfloat16() if v.dtype == torch.float else v for k, v in inputs.items()}
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            with torch.no_grad():
                res = model.generate(**inputs, **generate_kwargs)
            sentence = tokenizer.decode(res.tolist()[0], skip_special_tokens=True)
            ans.append(sentence)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output

