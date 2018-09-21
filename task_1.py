import requests
from urllib.parse import urlencode

APP_ID = 6698149
OAUTH_URL = 'https://oauth.vk.com/authorize'
oauth_data = {
    'client_id': APP_ID,
    #'redirect_uri': '',
    'display': 'page',
    'scope': 'status',
    'response_type': 'token'
}

print('?'.join((OAUTH_URL, urlencode(oauth_data))))

TOKEN = ''

class user:
    status = None
    id = None
    
    def __init__(self, token):
        self.token = token
        
    def get_params(self):
        return {
          'access_token': self.token,
          'v': '5.74'
        }
        
    def get_status(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/status.get', params)
        self.status = response.json()['response']['text']
        return self.status
        
    def set_status(self, text):
        params = self.get_params()
        params['text'] =  text
        response = requests.get('https://api.vk.com/method/status.set',params)
        if response.json()['response'] == 1:
            self.status = text
            return self.status
        return response.json()['response']
    
    def get_friend(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()['response']['items']
    
    def get_id(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/users.get', params)
        return response.json()['response'][0]['id']
    
    def __and__(self, other):
        friends_1 = self.get_friend()
        friends_2 = other.get_friend()
        common_friends = list()
        for friend in friends_1:
            if friend in friends_2:
                user_friend = user('')
                user_friend.id = friend
                common_friends.append(user_friend)
        return common_friends
        
    def __str__(self):
        if self.id == None:
            self.id = self.get_id()
        return 'https://vk.com/id' + str(self.id)
    
    

user_1 = user(TOKEN)
user_2 = user(TOKEN)

common_friends = user_1 & user_2
for friend in common_friends:
    print (friend)
