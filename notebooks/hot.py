import pandas as pd
from bs4 import BeautifulSoup
import requests

def scrape_hot100():
    """
    This function scrapes the Billboard Hot 100 list
    https://www.billboard.com/charts/hot-100/

    for the song title and the artist name

    :return:
    csv file
    """

    #url to scrape
    url = 'https://www.billboard.com/charts/hot-100/'

    #get response and print status
    response = requests.get(url)
    #print(response.status_code)

    #get soup
    soup = BeautifulSoup(response.text, 'html.parser')

    #print(soup.prettify())

    # get titles
    titles = []
    for song in soup.select('li h3'):
        titles.append(song.get_text().replace('\n','').replace('\t',''))

    titles = titles[:-9]

    artists = []
    for artist in soup.select('li ul li span.c-label')[0::7]:
        artists.append(artist.get_text().replace('\n','').replace('\t',''))

    top = pd.DataFrame({'titles':titles,
                        'artists': artists})



    top.to_csv('popular.csv', index=False)

if __name__ == '__main__':
    scrape_hot100()
