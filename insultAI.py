"""
Insult.AI is an API for predicting the offensiveness of insults. It takes a piece of text and returns a prediction of how insulting it is.  

Its built using hug, gunicorn and pyTorch. The model is trained on top of torchMoji [1] using transfer learning and the “Detecting Insults In Social Commentary” dataset [2]. 

[1] https://github.com/huggingface/torchMoji
[2] https://www.kaggle.com/c/detecting-insults-in-social-commentary/data
"""
import hug
import insultModel as m
import numpy as np 


@hug.post('/insult', output=hug.output_format.json )
def sentimentEndpoint( 
			text:hug.types.text, 
			language:hug.types.one_of([ 'en' ])='en',
			docType:hug.types.one_of(['PLAIN_TEXT'])='PLAIN_TEXT', 
		):
	
	"""Analyzes comments and predicts their offensiveness."""
	
	scores = m.score(text)
	return { 
	  "language": language ,
	  "sentences": scores
	 }


# test the endpoint
api = hug.API(__name__)
response = hug.test.post(api, '/insult', { "text": "You're so fake, Barbie is jealous. I like you. You are the worst" } ) 
print(response.data)
assert (response.status=='200 OK' and response.data is not None)
print( "SUCCESS" )
