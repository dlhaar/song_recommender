import pandas as pd
import numpy as np
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
import time
from dotenv import load_dotenv
import os

#input credentials
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def search_song(title:str, artist:str, limit=5) -> str:
    """
    Function takes two values: title and artist and then searches for it in Spotify
    It returns the number of results set by `limit`. 

    If the limit is great than 1, the user must select which item to pick.

    The function returns the Spotify id number.

    Input
    title: string of song title
    artist: string of artist name
    limit: the number of results to return

    Output
    string with Spotify song id number
    """
    

    #Initialize SpotiPy with user credentials #

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))

    try:
        #clean artist name
        artist = (artist.replace('Featuring', 'feat.')
                        .replace('X', '')
                        .replace('&', '')
                        .replace('x', '')            
                 )
        
        #search for song
        results = sp.search(q="artist:" + artist + " track:" + title, limit=limit)
    
        if limit > 1:
        #if len(results['tracks']['items']) > 1:
            #create a dataframe with the results
            select_dict = {}
            for i in range(len(results['tracks']['items'])):
                id = results['tracks']['items'][i]['id']
                select_dict[id] = [results["tracks"]["items"][i]['name'],
                                   results['tracks']['items'][i]['album']['artists'][0]['name'],
                                   results['tracks']['items'][i]['album']['name']]
                
            df_results = (pd.DataFrame.from_dict(select_dict,
                                                 orient='index',
                                                 columns = ['titles', 'artists', 'album'])
                          #.reset_index(names = 'id',
                           #            drop=False)
                          .drop_duplicates(subset = ['titles', 'artists', 'album'],
                                           keep='first')
                          .reset_index(names = 'id',
                                       drop=False)
                         )
            
            return(df_results)

        else:
            return results['tracks']['items'][0]['id']
        
    except IndexError:
        return 'Not found'



def get_audio_features(list_of_ids)->pd.DataFrame:
    """
    This function takes a list of id values and gets the spotify audio features for this song.
    The function returns a pandas DataFrame with the id number and the 

    Input
    list_of_ids: a list with id values as strings

    Output
    pandas DataFrame with the title of the song, name of the artist and all features
    """
    
    #Initialize SpotiPy with user credentias #
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                           client_secret=CLIENT_SECRET))
    full_dict={}
    for id in list_of_ids:
        my_dict = sp.audio_features(id)[0]
        
        full_dict[id] = my_dict
        
        time.sleep(1)
        
        
    features_df = pd.DataFrame.from_dict(full_dict,orient='index').reset_index(drop = True)

    features_df = features_df[['id', 'danceability', 'energy', 'acousticness', 'instrumentalness', 'tempo']]

    return features_df



def add_audio_features(df:pd.DataFrame, audio_features_df:pd.DataFrame) -> pd.DataFrame:
    """
    this function merges a dataframe containing the song title and artist with the song's features
    it returns the extended dataframe

    Input
    df: dataframe with song title, artist name, id
    audio_features_df: dataframe with id and features

    Output
    pandas dataframe with complete dataset
    """
    df_temp = df.copy()
    
    audio_features_df_temp = audio_features_df.copy()

    full_df = df_temp.merge(audio_features_df_temp, on = 'id', how = 'inner')

    return full_df


if __name__ == "__main__":
    search_song()
    get_audio_features()
    add_audio_features()




	






	