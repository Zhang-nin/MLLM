from model.instructblip import InstructBlipConfig, InstructBlipModel, InstructBlipPreTrainedModel,InstructBlipForConditionalGeneration,InstructBlipProcessor
import transformers
from PIL import Image
import torch
from get_Prompts import get
import os

def evaluate(arg):
    model_type = "instructblip"
    model_ckpt = "BleachNick/MMICL-Instructblip-T5-xxl"
    processor_ckpt = "Salesforce/instructblip-flan-t5-xxl"
    config = InstructBlipConfig.from_pretrained(model_ckpt)

    if 'instructblip' in model_type:
        model = InstructBlipForConditionalGeneration.from_pretrained(
            model_ckpt,
            config=config).to('cuda:0', dtype=torch.bfloat16)

    image_palceholder = "图"
    sp = [image_palceholder] + [f"<image{i}>" for i in range(20)]
    #     print("sp",sp)
    processor = InstructBlipProcessor.from_pretrained(
        processor_ckpt
    )
    sp = sp + processor.tokenizer.additional_special_tokens[len(sp):]
    processor.tokenizer.add_special_tokens({'additional_special_tokens': sp})
    if model.qformer.embeddings.word_embeddings.weight.shape[0] != len(processor.qformer_tokenizer):
        model.qformer.resize_token_embeddings(len(processor.qformer_tokenizer))
    replace_token = "".join(32 * [image_palceholder])

    prompt_teps = get(arg.task)
    output = []

    for img in os.listdir(arg.img_path):

        image = Image.open("Temp_file/11578.jpg")
        image1 = Image.open("Temp_file/944.jpg")
        image2 = arg.img_path + img
        images = [image, image1, image2]
        ans = []
        lab2 = prompt_teps[-1].split("C) ")[-1].split(".")[0]
        for question in prompt_teps:

            prompt = [
                f'Use the image 0: <image0>{replace_token},image 1: <image1>{replace_token} and image 2: <image2>{replace_token} as a visual content audit tool, it helps you accurately determine the category of your content. image 0 is {arg.task}.\nimage 1 is {lab2}.\n{question}"']
            prompt = " ".join(prompt)

            inputs = processor(images=images, text=prompt, return_tensors="pt")
            inputs['pixel_values'] = inputs['pixel_values'].to(torch.bfloat16)
            inputs['img_mask'] = torch.tensor([[1 for i in range(len(images))]])
            inputs['pixel_values'] = inputs['pixel_values'].unsqueeze(0)

            inputs = inputs.to('cuda:0')
            outputs = model.generate(
                pixel_values=inputs['pixel_values'],
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                img_mask=inputs['img_mask'],
                do_sample=False,
                max_length=50,
                min_length=1,
                set_min_padding_size=False,
            )
            generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
            ans.append(generated_text)
        res = {"id": img.split(".")[0], "answers": ans}
        output.append(res)
    return output





