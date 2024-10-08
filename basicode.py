from configparser import ConfigParser
import httpx

config = ConfigParser()
config.read('credentials.ini')
api_key = config['BingAPI']['api_key']
BingAPI = "https://api.bing.microsoft.com/v7.0/search"

web_search_endpoint = 'https://api.bing.microsoft.com/v7.0/search' 

headers = {
    'Ocp-Apim-Subscription-Key': api_key
}

query = 'openai'

params = {
    'q': query,
    'count': 50,
    'offset': 0,
    'mkt': 'en-US',
    'freshness': 'Month'
}
results = []
query = 'openai'
for i in range(0, 201, 50):
    params = {
    'q': query,
    'count': 50,
    'offset': i,
    'mkt': 'en-US',
    'freshness': 'Month'
    }
    response = httpx.get(web_search_endpoint, headers=headers, params=params)
    resultset = response.json()
    if 'webPages' in resultset and 'mainline' in resultset['webPages'] and 'items' in resultset['webPages']['mainline']:
        results.extend(resultset['webPages']['mainline']['items'])
    else:
        print(f"Expected keys not found in the response for offset {i}: {resultset}")

print(results)

# ========================================================================================================


# from configparser import ConfigParser
# import httpx
# import json
# from bs4 import BeautifulSoup

# # Load API key from credentials.ini
# config = ConfigParser()
# config.read('credentials.ini')
# api_key = config['BingAPI']['api_key']

# # Set up the Bing Web Search endpoint and headers
# bing_api_url = "https://api.bing.microsoft.com/v7.0/search"
# headers = {
#     'Ocp-Apim-Subscription-Key': api_key
# }

# # Get search query from user
# query = input("Enter your search query: ")

# # Initialize an empty list to store results
# results = []

# # Loop to gather results (paging through multiple results)
# for i in range(0, 150, 50):  # Adjust range and step as needed
#     params = {
#         'q': query,
#         'count': 50,  # Number of results to fetch per request
#         'offset': i,  # Skip results based on the offset
#         'mkt': 'en-US',
#         'freshness': 'Month'  # Get results from the last month
#     }
    
#     # Make the API request
#     response = httpx.get(bing_api_url, headers=headers, params=params)
#     resultset = response.json()
    
#     # Extract relevant information
#     if 'webPages' in resultset and 'value' in resultset['webPages']:
#         for item in resultset['webPages']['value']:
#             result = {
#                 'title': item.get('name'),
#                 'url': item.get('url'),
#                 'snippet': item.get('snippet'),
#                 'datePublished': item.get('datePublished', 'No date available') 
#             }
#             results.append(result)
#     else:
#         print(f"Unexpected structure: {resultset}")

# # Save the results to a JSON file (optional)
# with open('gathered_info.json', 'w') as f:
#     json.dump(results, f, indent=4)

# # Print the results
# for result in results:
#     print(f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['snippet']}\n")

# print(f"Total results: {len(results)}")