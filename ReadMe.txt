
-- Simple Guessing game --

To run locally on the same machine:
install httpserver, random, ast, requests packages using python pip3 package manager.

1. Start your server by running python script on one terminal.
python3 hangman.py

2. Open another terminal and import requests

3. send HTTP client request to start the game: 
res = requests.get("http://localhost:8000")

4. res.text 
Gives server response.
Gives more information on the new word to be guessed, chances left etc.

5. Now send your guess using requests.put method in json format.
res = requests.put("http://localhost:8000", json={'letter':'t'})

6. res.text
Gives server response for your guess.



