import requests


def fetch_movies():
    search_text = input('Enter movie to search: ')
    apikey='30d67521'
    url = f'https://omdbapi.com?apikey={apikey}&s={search_text}'

    resp = requests.get(url)
    
    if resp.status_code != 200:
        print('something went wrong check the message')
        print(resp.text)
        return
    
    data = resp.json()
    print(f'Found {data['totalResults']} movies/shows')
    print('Here are the first 10 movies/shows')
    for m in data['Search']:
        print(f'{m['Title']} - {m['Year']}')


if __name__ == '__main__':
    fetch_movies()