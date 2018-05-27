# insult.AI

Insult.AI is an API for predicting the offensiveness of insults. It takes a piece of text and returns a prediction of how insulting it the comment is.  


## Overview 
The API has one endpoint 

**Method** : `POST`
**ENDPOINT** : `/insult`

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

**Example Request**
```bash
curl -d "text=You're so fake, Barbie is jealous." -X POST http://[EXTERNAL_IP]:8000/insult
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
* [hug](https://github.com/timothycrosley/hug): Fast and lightweight Python web framework
* [Gunicorn](http://gunicorn.org/): Python Web Server Gateway Interface
* [torchMoji](https://github.com/huggingface/torchMoji): Emoji icons predictions
* [Insults Dataset](https://www.kaggle.com/c/detecting-insults-in-social-commentary): Insults in Social Commentary Dataset

The model is built in pyTorch, and trained on Kaggles "Insults in Social Commentary" dataset, using transfer learning.

The API handler is built in hug, then served through a Gunicorn Gateway Interface.

## Kubernetes Setup 

We can run the app using Googles Kubernetes Container Orchestrator, for fast and scalable deployment.

Build the docker file 
```bash
docker build -t insult-ai:latest .
```
Push the image to your Coogle cloud container registry,
```bash
docker tag insult-ai:latest eu.gcr.io/[PROJECT-ID]/insult-ai:latest
docker push eu.gcr.io/[PROJECT-ID]/insult-ai:latest
```
Crate a cluster and start the app,
```bash
gcloud container clusters create cluster-1 --num-nodes "2" 
kubectl run insult-ai --image eu.gcr.io/[PROJECT-ID]/insult-ai:latest --port 8000
```
Exspose the application 
```bash
kubectl expose deployment insult-ai --type "LoadBalancer"
```
Check its running
```bash
kubectl get service insult-ai
```
