import requests
from utils.resources import local_base_url, docker_base_url

def send_user_query(user_query):
    kalex_query_endpoint = f"{docker_base_url}/kalex/query_kalex"
    response = requests.get(kalex_query_endpoint, params={"user_prompt":user_query})
    
    if response.status_code == 200:
      kalex_response = response.json()
      return kalex_response["ai"]
    else:
      return "There was an error processing your request try again"