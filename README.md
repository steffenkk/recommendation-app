# recommendation-app
A pure python collaborative filtering recommendation model to produce a product recommendation for an e-commerce shop. Service can be called via REST API and is deployed in a Docker container.   

## Get up and running

### Prerequisites:
- Make sure to download the OnlinRetail.csv from https://www.kaggle.com/vijayuv/onlineretail/notebooks and place it into a dir called "data" in the project root

### Start the app in the project root (see prerequisites)
 ```console
 pip install .
 prep
 uvicorn main:app --app-dir ./src --host 0.0.0.0 --port 8083 --reload
 ```

 ### or, start in docker with no dependencies:

 ```docker run -p 8083:8083 steffenkk/recommender-app:latest```
### request recommendations (examples)

Fake a clients request to get a recommendation from the service:

```make curl USER=x```

Here x is an integer and a corresponding json file is in the users dir. The json content is needed, since it provides the past orders of the user for the recommendaiton. You can pass an arbitrary user to the model, but you must include his or her orders in the request body.


### visit api docs

Thanks to FastAPI, docs are automatically generated. You can access them here: \n

http://localhost:8083/redoc

## Tests and Evaluation

### run tests
```python -m pytest```

### run evaluation

This will split the data set into train (80 %) and test (20 %), run the Item to Item Similiarity with different model params, create recommendatoins for approximately 1300 users and compare the results to the test data. Subsequently Precision, Recall and F-Score will be calculated. 20 different runs will be conducted. This can take a long time. Go and get your self some coffee, lunch or both ^^. 

```python sricpts/evaluate.py```

## Whats happening behind the scenes:

checkout the diagrams in the docs. For instance uml sequence at API Call:

![](https://github.com/steffenkk/recommendation-app/blob/main/docs/Sequence.png?raw=true)
