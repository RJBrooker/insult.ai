# insult.AI

Insult.AI is an API for predicting the offensiveness of insults. It takes a piece of text and returns a prediction of how insulting it the comment is.  

## Overview 
The API has one endpoint 

**Method** : `POST`
**Endpoint** : `/insult`

**Data constraints**
```json
{
    "text": {
        "type": "Basic text / string value"
    },"language": {
        "type": "Accepts one of the following values: (en)",
        "default": "en"
    },"docType": {
        "type": "Accepts one of the following values: (PLAIN_TEXT)",
        "default": "PLAIN_TEXT"
    }
}
```

**Data example**
```json
{
	"text": "You're so fake, Barbie is jealous.",
}
```

**Request example**
```bash
curl -X POST http://35.234.131.171:8000/insult -d "text=Youre so fake Barbie is jealous."
```

**Success response**

```json
{
    "language": "en", 
    "sentences": [{
        "text": "You're so fake, Barbie is jealous.", 
        "score": 0.8516324162000001, 
        "message": "That's pretty harsh!"
    }]
 }
```


## Built With 
* [pyTorch](https://pytorch.org/): Python Deep learning framework
* [Insults Dataset](https://www.kaggle.com/c/detecting-insults-in-social-commentary): Kaggles Insults in Social Commentary Dataset
* [hug](https://github.com/timothycrosley/hug): Fast and lightweight Python web framework
* [Gunicorn](http://gunicorn.org/): Python Web Server Gateway Interface
* [torchMoji](https://github.com/huggingface/torchMoji): Emoji predictions

The model is built in pyTorch, and trained on Kaggles "Insults in Social Commentary" dataset. It utilizes transfer learning through the torchMoji model. 

The API handler is built in hug, then served through a Gunicorn Gateway Interface.

## Model Results 
The model had an accuracy of 0.8482 on the validation set. This is better than the leading Kaggle winner - however I used a different training-validation split, so the results are not directly comparable.

Below are some training examples and their scores, 

| Insult        | Comment           | Score  |
| ------------- |:-------------:| -----:|
| 1      | "Can you please crawl back in your pathetic little hole." | 0.9597 |
| 1     | "DUMB BITCH..!! DUMB BITCH..!! DUMB BITCH..!! DUMB BITCH..!!"    |   0.9572  |
| 1 | "I never said I was smart. In fact I'm a complete moron. Which goes to show just how stupid you are."      |    0.9571 |
| 1 | "You are a lying, libeling, loser." | 0.93300128 |
.... 
| 0 | "He makes me laugh :)" | 0.0193 | 
| 0 | "May the best team win this year, because the Bobcats will win it all next year." | 0.0138 |
| 0 | "The view was to die for! I love the Tour Eiffel..couldn't have been better." | 0.0123 |
| 0 | "I WOULD LOVE TO HEAR THAT SPEECH." | 0.0093 |


## Kubernetes Setup 

We can run the app using Googles Kubernetes Container Orchestrator, for fast and scalable deployment.

Build the docker file 
```bash
docker build -t insult-ai:latest .
```
Push the image to your Google cloud container registry,
```bash
docker tag insult-ai:latest eu.gcr.io/[PROJECT-ID]/insult-ai:latest
docker push eu.gcr.io/[PROJECT-ID]/insult-ai:latest
```
Create a cluster and start the app,
```bash
gcloud container clusters create cluster-1 --num-nodes "2" 
kubectl run insult-ai --image eu.gcr.io/[PROJECT-ID]/insult-ai:latest --port 8000
```
Exspose the application and check its running,
```bash
kubectl expose deployment insult-ai --type "LoadBalancer"
kubectl get service insult-ai
```

## To-do
- [ ] Exstend the training data
- [ ] Convert target variable to a continues scale
- [ ] Tune hyper parameters 
- [ ] Build an adversary network for insult generation 



