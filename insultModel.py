# -*- coding: utf-8 -*-

""" Use torchMoji to score texts for insult analysis.
The result is a value between 0-1 predicting how insulting the comment is.
"""

from __future__ import print_function, division, unicode_literals
import json, csv, datetime

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH
from textblob import TextBlob
from torchmoji.model_def import torchmoji_transfer,TorchMoji
import torch
from torchmoji.global_variables import NB_TOKENS, NB_EMOJI_CLASSES

PRETRAINED_PATH =  '/'.join(PRETRAINED_PATH.split('/')[:-1]) + '/insults_model_chain-thaw_1.bin'

# get torchmoji vocabulary
with open(VOCAB_PATH, 'r') as f:
	vocabulary = json.load(f)

## Maximum length of string 
maxlen = 30
nb_classes = 2

## load the tokenizer and pretrained model
st = SentenceTokenizer(vocabulary, maxlen)
model = torchmoji_emojis(PRETRAINED_PATH)

model = TorchMoji(nb_classes=2,nb_tokens=NB_TOKENS,)
model.load_state_dict(torch.load(PRETRAINED_PATH, ))

def message(score):
	if  score > 0.95: return "You are sick"
	elif score > 0.8: return "That's pretty harsh!"
	elif score > 0.5: return "Not very polite..."
	elif score > 0.25: return "Thanks..."
	elif score > 0.1: return "ok"
	else: return ':-)'

def get_sentences(doc):
	blob = TextBlob(doc)
	for sentence in blob.sentences:
		yield str(sentence)

def score(doc):
	sentences = list(get_sentences(doc))
	tokenized, _, _ = st.tokenize_sentences(sentences)
	prob = model(tokenized).astype(float)
	out = [ 
		{'text':  sentences[i] , 'score': float(prob[i][0]) , 'message': message(prob[i]) } \
		for i in range(len(sentences))  \
	]
	return out

