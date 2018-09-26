import requests
from urllib.parse import urlencode
import constants

#Вывод ссылке для получения ключа доступа к странице 
print('?'.join((constants.OAUTH_URL, urlencode(constants.oauth_data))))

#Ключ доступа к странице
TOKEN = ''


class User:
    '''
    Класс пользователь.
    Данный класс используетс для хранения данных о пользовтелях сети "В контакте".
    
    Данный класс хранит информацию о статусе пользователя, ссылку на страницу в интернете и ключ доступа к странице.
    
    Для создания объекта пользователь необходимо указать ключ доступа к странице.
        user = User(TOKEN)
        
    Оператор И возвращает список обших друзей пользователей.
        common_friends = user_1 & user_2
        
    Функция print() выводит ссылку на страницу пользователя.
    
    Методы класса пользователь:
        get_params() - возвращает ключ доступа к странице.
        get_status() - возвращает стутус пользователя.
        set_status(text) - устанавливает статус пользователя.
        get_friend() - возвращает список с id друзей пользоваиеля.
        get_id() - возвращает id пользователя.
    
    '''
    
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
        self.id = response.json()['response'][0]['id']
        return response.json()['response'][0]['id']
    
    def __and__(self, other):
        friends_1 = self.get_friend()
        friends_2 = other.get_friend()
        common_friends = list()
        for friend in friends_1:
            if friend in friends_2:
                user_friend = User('')
                user_friend.id = friend
                common_friends.append(user_friend)
        return common_friends
        
    def __str__(self):
        if self.id == None:
            self.id = self.get_id()
        return 'https://vk.com/id' + str(self.id)
    
    
user_1 = User(TOKEN)
user_2 = User(TOKEN)

common_friends = user_1 & user_2
for friend in common_friends:
    print (friend)
