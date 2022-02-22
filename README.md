# Twitter Bot v1.0.0
This script queries Twitter for tweets using their API.
The results are saved in a .csv file in a formatted way.
Various filters are applied to find the desired tweets.

#

## Installation
<br/>

This project uses **Python 3.9.6**

Clone the project:
```
git clone https://github.com/ivandimitrovkyulev/TwitterBot.git

cd TwitterBot
```

Create a virtual environment in the current working directory and activate it:

```
python3 -m venv <current-directory>

source <current/directory>/bin/activate
```

Install all third-party project dependencies:
```
pip install -r requirements.txt
```

You will also need to save the following variables in a **.env** file in the same directory:
```
API_KEY=<your-api-key> 

API_SECRET_KEY=<your-api-secret>

ACCESS_TOKEN=<your-access-token>

ACCESS_TOKEN_SECRET=<your-access-token-secret>
```

Which you can request from https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api

<br/>

## Running the script
<br/>

For help, please refer to the documentation:
```
python TwitterScrapper.py -h