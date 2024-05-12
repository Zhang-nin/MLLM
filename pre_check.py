def get_label(arg):
    tasks = ["misogyny", "shaming", "stereotype", "objectification","violence"]
    lab = {}

    with open(arg.label + "test.jsonl", "r") as r:
        for line in r.readlines():
            line = eval(line)
            if isinstance(line["label"],int):
                lab[str(line["id"])] = line["label"]
            else:
                lab[str(line["id"])] = line["label"][tasks.index(arg.task)]

    return lab

def get_ans(sens):
    if len(sens) == 1:
        if sens == "A":
            return 1
        elif sens == "B":
            return 0
        return 2
    elif "A:" in sens or "A " in sens or "A)" in sens or "A." in sens or "yes" in sens:
        return 1
    elif "B:" in sens or "B " in sens or "B)" in sens or "B." in sens or "no" in sens:
        return 0
    elif "C:" in sens or "C " in sens or "C)" in sens or "C." in sens:
        return 2
    return 2

def get_ans1(sens):
    if len(sens) == 1:
        if sens == "A":
            return 0
        elif sens == "C":
            return 1
        return 2
    elif "A:" in sens or "A " in sens or "A)" in sens or "A." in sens or "yes" in sens:
        return 0
    elif "B:" in sens or "B " in sens or "B)" in sens or "B." in sens or "no" in sens:
        return 2
    elif "C:" in sens or "C " in sens or "C)" in sens or "C." in sens:
        return 1
    return 2

def get_ans2(sens):
    if len(sens) == 1:
        if sens == "C":
            return 0
        elif sens == "B":
            return 1
        return 2
    elif "A:" in sens or "A " in sens or "A)" in sens or "A." in sens or "yes" in sens:
        return 2
    elif "B:" in sens or "B " in sens or "B)" in sens or "B." in sens or "no" in sens:
        return 1
    elif "C:" in sens or "C " in sens or "C)" in sens or "C." in sens:
        return 0
    return 2

def check(pres, arg):
    lab = get_label(arg)
    acc1 = [0] * 3
    acc2 = [0] * 3
    for pre in pres:
        for i,ans in enumerate(pre["answers"]):
            if i == 0:
                res = get_ans(ans)
            elif i == 1:
                res = get_ans1(ans)
            else:
                res = get_ans2(ans)
            # ACC
            if lab[str(pre["id"])] == res:
                acc1[i] += 1
            # Avoidance Rate
            if 2 == res:
                acc2[i] += 1
    return {"ACC":sum(acc1) / (3*len(lab)) * 100,"Avoidance Rate":sum(acc2) / (3*len(lab)) * 100}


