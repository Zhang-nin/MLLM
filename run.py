import argparse
from pre_check import check
PATH = "Datasets/"
Task2Data = {"unethical":"ELEMENT","harmful(CN)":"CHMEMES","harmful":"Harm-C","hateful":"HMC","offensive":"MultiOFF","misogyny":"Misogyny","shaming":"Misogyny","stereotype":"Misogyny","objectification":"Misogyny","violence":"Misogyny"}
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="Qwen-VL")
    parser.add_argument("--task", type=str, default="unethical")
    args = parser.parse_args()

    if args.model == "Qwen-VL":
        from MLLM.QwenVL import evaluate
    elif args.model == "MoE-LLaVA":
        from MLLM.MoELLaVA import evaluate
    elif args.model == "MiniCPM-V":
        from MLLM.MiniCPMV import evaluate
    elif args.model == "XComposer2":
        from MLLM.XComposer2 import evaluate
    elif args.model == "mPLUG_Owl":
        from MLLM.mplugowl import evaluate
    elif args.model == "VisualGLM":
        from MLLM.mplugowl import evaluate
    elif args.model == "XComposer":
        from MLLM.xcomposer import evaluate
    elif args.model == "instructblip":
        from MLLM.instructblip import evaluate
    elif args.model == "mPLUG_Owl2":
        from MLLM.mPLUGOwl2 import evaluate
    elif args.model == "Blip2":
        from MLLM.blip2 import evaluate
    elif args.model == "VisCpm":
        from MLLM.VisCPM import evaluate
    elif args.model == "MMICL":
        from MLLM.MMICL import evaluate
    elif args.model == "LLaVA":
        from MLLM.LLaVA import evaluate
    elif args.model == "CogVLM":
        from MLLM.CogVLM import evaluate
    else:
        from MLLM.IDEFICS import evaluate

    tasks = ["misogyny", "shaming", "stereotype", "objectification", "violence"]
    args.__setattr__('img_path', PATH + Task2Data[args.task] + "/img/")
    args.__setattr__('label', PATH + Task2Data[args.task] + "/")
    output = evaluate(args)
    result = check(output, args)
    print(result)

