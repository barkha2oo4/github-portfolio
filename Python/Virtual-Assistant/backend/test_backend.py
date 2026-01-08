from dotenv import load_dotenv
load_dotenv()

import requests

def test_query(query):
    url = 'http://127.0.0.1:5000/query'
    response = requests.post(url, json={'input': query})
    print(f'Query: {query}\nResponse: {response.json().get("response")}\n')

if __name__ == '__main__':
    test_query('What is the weather in London?')
    test_query('Define serendipity')
    test_query('Remind me to call John at 5pm')
    test_query('Hello!')
    test_query('Who is the president of France?')
