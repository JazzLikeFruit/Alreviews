# Alreviews

This flask application implements a rating system for albums. The application uses the spotipy library and Spotify api to gather information
about albums and users are able to rate each songs and thus create a rating for an album. Users can also listen to every song in the album while doing this. To be albe
to use this feature the user needs a spotify premium subscription.

## Screencast

[![Screencast](https://img.youtube.com/vi/NejknOsAoTA/0.jpg)](https://www.youtube.com/watch?v=NejknOsAoTA)

## Problem statement

After listening to an album most of the times my friends ask me what I think of it and all i can answer is "I liked it" or "I hated it". With this application I'd like to create a way to be more critical with the albums I listen to and formulate a better oppinion about albums I've listened to in the past.

## Solution description

With the app I will be able to look up a sertain album by an artist, listen to the songs, answer questions about what I thought about a song and the entire album and this will generate a grade and this will be added to a list of albums I've graded before.

## Data sources

The data sources that will be used to gather the neesded information are:

- Spotify: Spotify (Swedish media services provider and music streaming service) will be used to gather all the infomation about the albums.

## External components

To implement this application I will be using:

- Spotipy library: This will be used to pull the infomation form the spotify API
- Spotify Web Playback SDK: This will be used to create a web player and play selected albums
- Flask: to create the server
- SQLalchemy: to create the database
- Bootstrap/CSS: to style the application
- flask_spotify_auth: library that handles spotify user authentication (https://github.com/vanortg/Flask-Spotify-Auth)

## Details and sketches

### Homepage

The first page of the application is the homepage. On this page the user will be able to
search for an album by filling in the textbox and pressing the seach button. The user can also
go to the user profile by pressing the icon in the navbar.

## ![homepage](doc/1.JPG)

### Search result

The second page displays the search result from the user's query. This page loads the name,
artist and basic information of every album related to the user query. the user can select an album
to review by pressing the review button.

## ![search result](doc/2.JPG)

### Album page

This page firstly displays basic information about the selected ablum. Thereafter the user is presented
with the tracklist of set album and a textbox inwhich the user can rate a song. This is followed by
a textbox where the user can leave their thoughts about the album.

## ![Album page](doc/3.JPG)

### User page

On this page the user can see their reviewed album.

## ![User profile](doc/4.JPG)

## Similar applications

The application that I found that lightly resembles Alreviews is:

Rateyourmusic.com: On this application the average rating of an sertain album by an user determines the
total score displayed on the website. To do this users are devided in different ranks determined by their traffic
on the website. This rank determines the weight of a review by an user.

Alreviews will in the contrary be a site on which users can determine their personal oppinion on an album and compare this
to their oppinions of other albums.

## Hardest parts

The hardest parts to implement will be:

- Perfoming the API requests to spotify
- Creating the webplayer
- calculating the ratings
- Making the UI
- Handeling user authentication
