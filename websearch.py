import os
from configparser import ConfigParser
import httpx
import pandas as pd
from bs4 import BeautifulSoup

# Load API key from credentials.ini
config = ConfigParser()
config.read('credentials.ini')
api_key = config['BingAPI']['api_key']

# Set up the Bing Web Search endpoint and headers
bing_api_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {
    'Ocp-Apim-Subscription-Key': api_key
}

# Get search query from user
query = input("Enter your search query: ")

# Replace spaces with underscores for the filename
safe_query = query.replace(' ', '_')
filename = f'{safe_query}.xlsx'

# Create directory if it doesn't exist
folder_name = 'parsedData'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Define the full path for the file
excel_file = os.path.join(folder_name, filename)

# Define the number of results to fetch per request
results_per_request = 50

# Initialize an empty list to store results
results = []

# Loop to gather results (paging through multiple results)
for offset in range(0, 301, results_per_request):  # Adjust range as needed
    params = {
        'q': query,
        'count': results_per_request,  # Number of results to fetch per request
        'offset': offset,  # Skip results based on the offset
        'mkt': 'en-US',
        'freshness': 'Month'  # Get results from the last month
    }
    
    # Make the API request
    response = httpx.get(bing_api_url, headers=headers, params=params)
    resultset = response.json()
    
    # Extract relevant information
    if 'webPages' in resultset and 'value' in resultset['webPages']:
        for item in resultset['webPages']['value']:
            url = item.get('url')
            title = item.get('name')
            snippet = item.get('snippet')
            date_published = item.get('datePublished', 'No date available')
            
            # Fetch and parse the content of the webpage
            webpage_content = ''
            try:
                webpage_response = httpx.get(url)
                soup = BeautifulSoup(webpage_response.text, 'html.parser')
                # Example: Extracting the text from <p> tags
                paragraphs = soup.find_all('p')
                webpage_content = ' '.join([para.get_text() for para in paragraphs])
            except Exception as e:
                webpage_content = f"Failed to fetch content: {e}"
            
            result = {
                'Title': title,
                'URL': url,
                'Snippet': snippet,
                'Date Published': date_published,
                'Content': webpage_content  # Add content of the webpage
            }
            results.append(result)
        
        # If fewer results are returned than requested, break the loop
        if len(resultset['webPages']['value']) < results_per_request:
            break
    else:
        print(f"Unexpected structure: {resultset}")
        break

# Convert results to a DataFrame and save to an Excel file
df = pd.DataFrame(results)
df.to_excel(excel_file, index=False)

print(f"Results have been saved to {excel_file}")
