import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from config import comunity_token, acces_token
from core2 import VkTools
from DataBase import insert_data_seen_person,delete_table_seen_person,check,insert_data_seen

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
                    if self.params == None:
                        self.message_send(event.user_id, 'давайте сперва познакомимся. введите команду"привет"')
                    else:
                             
                        users = self.api.serch_users(self.params)
                        Veiwed = []
                        for row in check():                                                
                            Veiwed.append(row)
                        print(Veiwed)    
                        View=len(Veiwed)
                        if View !=0:
                                    
                                    for user in users:
                                            userid=user['id']
                                            for names in Veiwed:
                                                    named=int(names[1])
                                                    if userid==named:
                                                        users.remove(user)
                                
                                                                  
                                                            


                        index=len(users)
                        index-=1
                        user = users.pop(index)
                    
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
                        insert_data_seen(user_name)
                             

                elif command == 'дальше':
                    index-=1 
                    user = users.pop(index)   
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
                    if index==0:
                     self.message_send(event.user_id,   
                                       f'Все анкеты просмотренны. Выполните новый поиск ',
                                       attachment=None
                                       )
                elif command == 'пока':
                    self.message_send(event.user_id, 'пока')
                    delete_table_seen_person()
                else:
                    self.message_send(event.user_id, 'команда не опознана')
             
if __name__ == '__main__':
    bot = BotInterface(comunity_token, acces_token)
    bot.event_handler()
