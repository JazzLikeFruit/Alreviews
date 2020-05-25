# Design

This document explains the problem in a more technical fashion.

## Features

The features users of this app will be able to use are:

1. Log into spotify account
2. Search for albums
3. Load results from user query
4. Read information about an album
5. Listen to the album
6. score each song if an album
7. review rated albums

## User interface

These are the following screens that will be available to make use of the features.

### Login screen

This page will implement the the first feature where the user logs into their spotify account.

On execution, the user is redirected to a page where the requested information is presented. the user has to log into their spotify account. After this they will be rederected to the homepage.

This is used to gain permission from the user to create a Spotify acces token. This token is used to make API requests and create the Spotify player.

![Login](doc/login.PNG)

Uses:

- Spotipy library
- Spotify API

Reference: https://developer.spotify.com/documentation/general/guides/authorization-guide/

### Homepage

On this page the user can search for an album by filling the textbox and pressing the search icon. This implements the second feature in the features list.

By pressing the button a API request is sent to gather all albums where the user query appears.

![Homepage](doc/Search.PNG)

Uses:

- Spotipy library

### Search result

On this page the search results gathered from the user query are displayed. this implements the third feature in the features list.

![Search](doc/result.PNG)

Uses:

- Spotipy library

### Album page

This page implements the fourth, fifth and sixth feature from the list. On this page the user firstly sees infomation about an album. By pressing the play button behind a song in the tracklist the play is loaded and the user can listen to set song.

After listening and rating each song the user can press the rate button whereafter the user will be rederected to the User page.

![Album](doc/album.PNG)

Uses:

- Spotipy library
- Spotify Web Playback SDK

Reference: https://developer.spotify.com/documentation/web-playback-sdk/

### User page

On this page the user can view their reviewed album hereby implementing the seventh feature.

This is done by loading the information from the database.

![User](doc/user.PNG)

## Database

The following diagram shows how the database will be designed.

![Database](doc/classdiagram.PNG)

## Detailed list

the following list contains a detailed view of the API's and frameworks that will be used.

### Spotify Platform

Spotify API:
This API is used to gather information about an album. for this the following is needed:

- Creation: To use the spotify api the app has to be registered.
- Autorization: this is needed to gain access to the data. Alreviews will use the Autorization flow where the user autorized the use of their account once and this is used untill the user logs back out.
- API requests: This is used to load the information. To do this the spotiy library will be used.

### Spotipy library

This is a Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform. This liberary will be used to make the API request to the spotify platform.

### Web Playback SDK

This is a client-side JavaScript library which allows the creation of a new player in Spotify Connect and playing any audio track from Spotify in the browser via Encrypted Media Extensions.

To create this the access token that is returned after the user logs in is needed.
