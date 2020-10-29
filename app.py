import os
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd

st.title("Music Recommendation from SPOTIFY")

#getting spotify credentials
load_dotenv(find_dotenv())
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

#spotify recommendation

navBar = st.sidebar.radio("Navigation", ["Recommend by Search", "Recommend by Year"])

if navBar == "Recommend by Search":
    searchStr = st.text_input('Input any movie, genre, or artist...')

    if searchStr:
        artistName1 = []
        trackName1 = []
        popularityScore1 = []
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
        searchResult = sp.search(q = searchStr, limit = 1, offset = 50)
        list_ids = [searchResult['tracks']['items'][0]['id']]
        for ids in range(0, 10, 1):
            suggestions = sp.recommendations(seed_tracks=list_ids, limit = 10, offset = 10)
            for ids, track in enumerate(suggestions['tracks']):
                trackName1.append(suggestions['tracks'][ids]['name'])
                artistName1.append(suggestions['tracks'][ids]['artists'][0]['name'])
                popularityScore1.append(suggestions['tracks'][ids]['popularity'])

        df_recommend = pd.DataFrame({'artistName':artistName1, 'songName': trackName1,
        'Popularity Score': popularityScore1})
        #df_recommend.drop_duplicates(inplace = True)
        df_recommend = df_recommend.sort_values(by=['Popularity Score'], ascending = False)
        df_recommend.drop_duplicates(inplace = True)
        df_recommend.reset_index(inplace = True)
        df_recommend.drop(columns =['index'], inplace = True)
        df_recommend = df_recommend.head(10)
        st.table(df_recommend.set_index('artistName'))

if navBar == "Recommend by Year":
    searchYr = st.selectbox('Select a year to get music recommendation!', ('','2016', '2017', '2018', '2019', '2020'))
    if len(searchYr)==4:
        artistName = []
        songName = []
        popularityScore = []
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
        for i in range(0,1000,50): 
            searchResult = sp.search(q = 'year:' + searchYr, type = 'track', limit = 50, offset=50)
            for i, j in enumerate(searchResult['tracks']['items']):
                artistName.append(j['artists'][0]['name'])
                songName.append(j['name'])
                popularityScore.append(j['popularity'])

        df_tracks = pd.DataFrame({'artistName':artistName, 'songName': songName,
        'popularityScore': popularityScore})
        df_tracks = df_tracks.sort_values(by=['popularityScore'], ascending = False)
        df_tracks.drop_duplicates(inplace = True)
        df_tracks.reset_index(inplace = True)
        df_tracks.drop(columns =['index'], inplace = True)
        st.dataframe(df_tracks.set_index('artistName'))


