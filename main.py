import json

import torch
from transformers import T5Tokenizer, AutoModelForCausalLM
from flask import (
    Flask, request
)


LABEL = ["相手:", "自分:"]
TARGET_LENGTH, SENTENCE_NUM = 30, 10


tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt-1b")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")
#model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b").to('cuda')


def get_sentences(text, generate_length, num_return_sequences):
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")
    #token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt").to('cuda')

    input_length = len(token_ids[0])
    with torch.no_grad():
        output_ids = model.generate(
            token_ids,
            do_sample=True,
            max_length=input_length+generate_length,
            min_length=input_length+generate_length,
            num_return_sequences=num_return_sequences,
            top_k=500,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_word_ids=[[tokenizer.unk_token_id]]
        )
    sentences = tokenizer.batch_decode([tokens[input_length:] for tokens in output_ids.tolist()])

    return sentences


def choose_sentence(sentences):
    output, closest_distance = "", TARGET_LENGTH

    for i, sentence in enumerate(sentences):
        if LABEL[0] not in sentence:
            continue
        tmp = sentence.split(LABEL[0])
        reply = tmp[0]
        if ':' in reply or '(' in reply or '返事をする' in reply:
            continue
        distance = abs(TARGET_LENGTH - len(reply))
        if distance < closest_distance:
            closest_distance = distance
            output = reply

    return output


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/chitchat', methods=['POST'])
def chitchat():
    if request.method == 'POST':
        contexts = request.json['contexts']
        QUESTION = \
"""
相手に返事をする

"""

        concat = []
        for i, s in enumerate(contexts):
            concat.append(LABEL[i%2] + s)
        concat.append(LABEL[1])
        input = QUESTION + "\n".join(concat)
        sentences = get_sentences(input, TARGET_LENGTH, SENTENCE_NUM)
        output = choose_sentence(sentences)
        return output


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8001, debug=True)
