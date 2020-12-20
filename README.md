# recommendation-app
A pure python collaborative filtering recommendation model to produce a product recommendation for an e-commerce shop. Service can be called via REST API and is deployed in a Docker container.   

## Get up and running
### Start the app in the project root (see prerequisites)
 ```uvicorn main:app --app-dir ./src --host 0.0.0.0 --port 8083 --reload```

 ### or, start in docker with no dependencies:

 ```docker run -p 8083:8083 steffenkk/recommender-app:latest```
### request recommendations (examples)

Fake a clients request to get a recommendation from the service:

```make curl USER=x```

Here x is an integer and a corresponding json file is in the users dir. The json content is needed, since it provides the past orders of the user for the recommendaiton. You can pass an arbitrary user to the model, but you must include his or her orders in the request body.


### Prerequisites:
- Make sure to download the OnlinRetail.csv from https://www.kaggle.com/vijayuv/onlineretail/notebooks and place it into the data folder in the project root dir
