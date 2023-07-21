import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import comunity_token, acces_token
from core2 import VkTools
from DataBase import insert_data_seen_person,delete_table_seen_person



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
                    self.message_send(event.user_id, f'здравствуй {self.params["name"]}')
                elif command == 'поиск':
                    users = self.api.serch_users(self.params)
                    ind=len(users)
                    ind-=1
                    user = users.pop(ind)
                                      
                    
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
                    
                    insert_data_seen_person(id_vk=user['id'])

                elif command == 'дальше':
                    ind-=1 
                    user = users.pop(ind)   
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
                    if ind<0:
                     self.message_send(event.user_id,   
                                       f'Все анкеты просмотренны. Выполните новый поиск ',
                                       attachment=None
                                       )
                elif command == 'пока':
                    self.message_send(event.user_id, 'пока')
                    delete_table_seen_person()
                else:
                    self.message_send(event.user_id, 'команда не опознана')

    """def show_found_person(self):
        print(bot.serch_users(params))
        if self.get_found_person_id() == None:
            self.message_send(user_id,
                          f'Все анекты ранее были просмотрены. Выполните новый поиск. '
                          )
        else:
            ins_data(self.get_found_person_id())
            """


if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
""" vkid=[]
                    for photo in photos_user:
                        id_vk=photo["owner_id"]
                        vkid.append(photo["owner_id"])
                        insert_data_seen_person(id_vk)"""
""""photo_user=[]
                    for i in check():
                        photo_user.append(int(i[0]))"""
                    
"""max_count=len(photo_user)
                    for index in range(len(photo_user)):
                            value = photo_user[index]
                            return value """