# This is a new file for integrating with external APIs
# We will define functions to fetch data from weather, news, recreation APIs, etc.

def fetch_weather(location):
    """
    Function to fetch weather data based on location.
    Replace 'your-api-key' and 'api-endpoint' with your actual API key and endpoint URL.
    """
    api_key = "your-api-key" 
    base_url = "api-endpoint"
  
    # complete API URL 
    complete_url = base_url + "appid=" + api_key + "&q=" + location 
  
    # get method of requests module 
    # return respose object
    response = requests.get(complete_url)   
  
    # json method of response object to convert json format data into python format data 
    data = response.json() 
  
    return data

def fetch_news(topic):
    """
    Function to fetch news data based on a specific topic.
    Replace 'your-api-key' and 'api-endpoint' with your actual API key and endpoint URL.
    """
    api_key = "your-api-key"
    base_url = "api-endpoint"

    # complete API URL
    complete_url = base_url + "everything?q=" + topic + "&apiKey=" + api_key

    # get method of requests module
    # return response object
    response = requests.get(complete_url) 
    
    # json method of response object to convert json format data into python format data
    data = response.json()
  
    return data