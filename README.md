*Prerequisite - must have a Spotify premium account

## 1) Create a config.toml file at the root directory with the following variables:


`[setlist]`

`api_key = xxx`


`[spotify]`

`client_id = xxx`

`redirect_uri = "https://www.setlist.fm/"`

`scope = "user-read-private,playlist-modify-public"`

You will need to generate an API key for Setlist.fm by signing up, creating an account then requesting one from your account: https://www.setlist.fm/settings/apps

You will need to generate a client ID for Spotify by going to: https://developer.spotify.com/. Log in with your Spotify credentials and create an app project. Under 'Settings' - 'Basic Information' an ID can be found. You will also need to input the same redirect uri you have in the config file, in the relevant field on that page too.


## 2) Run the script from a CLI. 


When you are in the local working directory, run `python create_playlist.py`

It will then prompt you to copy and paste the setlist ID for the setlist you want to make a Spotify playlist from. You can find this in the url of the setlist page on setlist.fm

![image](https://github.com/user-attachments/assets/6aab66e1-2421-4a35-a886-5df10c8d2794)

Paste the ID and enter on the CL. The script should then run and if it is the first time it will open the Spotify auth window in your browser. Give permission for the app to create a playlist on your Spotify account and it should then redirect you to the setlist.fm home page,
and the url will have a code appended to it. 

![image](https://github.com/user-attachments/assets/9e23da57-8d85-4b01-9509-837366e37f8a)

The CL will ask you to copy and paste the full url (copy and paste all of it not just the code part). It will then continue with the script and either throw an error or confirm that a playlist has been created.


