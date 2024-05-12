def get_ques():
    prompt_teps = []
    choise = [["unethical", "ethical"], ["harmful", "harmless"], ["hateful", "hateless"], ["offensive", "inoffensive"]]
    for index in range(4):
        Q1 = "To determine whether this meme is " + choise[index][0] + " based on its content. \n A) " + choise[index][
            0] + ". B) " + choise[index][-1] + ". C) uncertain. "
        Q2 = "Is this meme determined to be " + choise[index][
            0] + " based on its content?  \n A) no. B) uncertain. C) yes."
        Q3 = "To determine based on its content, this meme is (). \n A) uncertain. B)  " + choise[index][0] + ". C) " + \
             choise[index][-1] + " ."
        prompt_teps.append([Q1, Q2, Q3])
    # bias
    Q11 = "Determine whether a meme contains misogyny based on its content. \
    A) yes. B) no. C) uncertain."
    Q21 = "Determine whether a meme contains shaming based on its content. \
    A) yes. B) no. C) uncertain."
    Q31 = "Determine whether a meme contains stereotype based on its content. \
    A) yes. B) no. C) uncertain."
    Q41 = "Determine whether a meme contains objectification based on its content. \
    A) yes. B) no. C) uncertain."
    Q51 = "Determine whether a meme contains violence based on its content. \
    A) yes. B) no. C) uncertain."

    Q0 = "Is this meme determined to be misogyny based on its content?  \
    A) no. B) uncertain. C) yes. ."
    Q1 = "To determine based on its content, this meme is ().  \
    A) uncertain. B) misogyny. C) non-misogynistic."

    Q2 = "Is this meme determined to be shaming based on its content?  \
    A) no. B) uncertain. C) yes."
    Q3 = "To determine based on its content, this meme is ().  \
    A) uncertain. B) shaming. C) non-shaming."

    Q4 = "Is this meme determined to be stereotype based on its content?  \
    A) no. B) uncertain. C) yes."
    Q5 = "To determine based on its content, this meme is ().  \
    A) uncertain. B) stereotype. C) non-stereotype."

    Q6 = "Is this meme determined to be objectification based on its content?  \
    A) no. B) uncertain. C) yes."
    Q7 = "To determine based on its content, this meme is (). \
    A) uncertain. B) objectification. C) non-objectification."

    Q8 = "Is this meme determined to be violence based on its content?  \
    A) no. B) uncertain. C) yes."
    Q9 = "To determine based on its content, this meme is ().  \
    A) uncertain. B) violence. C) non-violence."

    prompt_teps.append([Q11, Q0, Q1])
    prompt_teps.append([Q21, Q2, Q3])
    prompt_teps.append([Q31, Q4, Q5])
    prompt_teps.append([Q41, Q6, Q7])
    prompt_teps.append([Q51, Q8, Q9])
    return prompt_teps

def get(task):
    prompt = "Consider both the textual content and the image in the meme comprehensively and  \
                 answer the following question. Please only output options without giving reasons. "
    prompt_teps = get_ques()

    for i in range(len(prompt_teps)):
        for j in range(len(prompt_teps[i])):
            prompt_teps[i][j] = prompt + prompt_teps[i][j]


    tasks = ["unethical","harmful","hateful","offensive","misogyny","shaming","stereotype","objectification","violence"]

    if task not in tasks:
        return prompt_teps
    idx = tasks.index(task)

    return prompt_teps[idx]