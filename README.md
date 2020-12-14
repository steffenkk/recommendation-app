# recommendation-app
A pure python collaborative filtering recommendation model to produce a product recommendation for an e-commerce shop. Service can be called via REST API and is deployed in a Docker container.   
### Start the app in the src dir 
 ```uvicorn main:app --reload```

### Prerequisites:
- Make sure to download the OnlinRetail.csv from https://www.kaggle.com/vijayuv/onlineretail/notebooks and place it into a data folder in the project root dir