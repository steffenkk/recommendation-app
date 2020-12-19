.PHONY: curl

URL=http://localhost:8083/recommendations/

curl:
	curl --header "Content-Type: application/json" --request GET \
	 --data @./users/${USER}.json \
	'${URL}?user_id=${USER}' 
	
