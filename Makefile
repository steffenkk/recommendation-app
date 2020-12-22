.PHONY: curl, start

URL=http://localhost:8083/recommendations/

curl:
	curl --header "Content-Type: application/json" --request GET \
	 --data @./users/${USER}.json \
	'${URL}?user_id=${USER}' 

start:
	uvicorn main:app --app-dir ./src --host 0.0.0.0 --port 8083 --reload
	
