import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import comunity_token, acces_token
from core2 import VkTools
from DataBase import insert_data_seen_person,delete_table_seen_person,check

class BotInterface():


    def __init__(self,comunity_token, acces_token):
        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VkTools(acces_token)
        self.params = None

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                                {'user_id': user_id,
                                'message': message,
                                'attachment': attachment,
                                'random_id': get_random_id()
                                }
                                )
        
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)
        
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, 
                                      f'здравствуй {self.params["name"]}.кого ищем:введите "м или ж"')
                    print(self.params)
                
                elif command == 'м':
                    self.params['sex']=1
                    self.message_send(event.user_id, 
                                      f'ну давай искать. пиши "поиск')

                elif command == 'ж':
                    self.params['sex']=2
                    self.message_send(event.user_id, 
                                      f'ну давай искать. пиши "поиск')    
                       
                elif command == 'поиск':
                    if self.params == None:
                        self.message_send(event.user_id, 
                                          f'давайте сперва познакомимся. введите команду"привет"')
                    
                    elif self.params['city']== None:
                        self.message_send(event.user_id, 
                                          f'как называется город в котором вы проживаете?')
                        self.params['city']= command
                    
                    elif self.params['age']== None:
                        self.message_send(event.user_id, 
                                          f'напишите свой возраст цифрами')
                        self.params['age']= int(command)

                    else:
                        users = self.api.serch_users(self.params)
                        print('вот что нашли')
                        print(users)
                        Veiwed = []
                        for row in check():                                                
                            Veiwed.append(int(row[1]))
                        print(Veiwed)    
                        View=len(Veiwed)
                        count=len(users)
                        if View !=0:
                            while True:
                                if count>0:
                                    for user in users:
                                        if user['id'] in Veiwed:
                                            users.remove(user)
                                        count-=1
                                else:
                                    break        
                        print(users)
                        print(count)
                        
                        if len(users)>0:
                            print('вот что осталось')
                            print(users)
                            user = users.pop()
                            index=len(users)
                            print(index)
                    
                            photos_user = self.api.get_photos(user['id'])                  
                   
                            attachment = ''
                            for num, photo in enumerate(photos_user):
                                attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                                if num == 2:
                                    break
                            self.message_send(event.user_id,
                                      f'Встречайте {user["name"]}',
                                      attachment=attachment
                                      )
                             
                            id_vk=user["id"]
                            user_name=user["name"]
                            print(id_vk)
                            print(user_name)
                            insert_data_seen_person(id_vk)
                            
                        else:
                            self.message_send(event.user_id,   
                                       f'никого нет. попробуйте еще раз ',
                                       attachment=None
                                       )
                        
                             

                elif command == 'дальше':
                    print(index)
                    if index<=1:
                     self.message_send(event.user_id,   
                                       f'Все анкеты просмотренны. Выполните новый поиск ',
                                       attachment=None
                                       )
                    else:
                        user = users.pop()
                        index-=1   
                        photos_user = self.api.get_photos(user['id'])                  
                                            
                        attachment = ''
                        for num, photo in enumerate(photos_user):
                            attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                            if num == 2:
                                break
                        self.message_send(event.user_id,
                                      f'Встречайте {user["name"]}',
                                      attachment=attachment
                                      )        
                    
                elif command == 'пока':
                    self.message_send(event.user_id, 
                                      f'пока')
                    delete_table_seen_person()
                else:
                    self.message_send(event.user_id, 
                                      f'команда не опознана')
             
if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
