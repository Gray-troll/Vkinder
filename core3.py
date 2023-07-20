from config import  acces_token
from core2 import VkTools
from DataBase import check,insert_data_seen_person

bot = VkTools(acces_token)
params = bot.get_profile_info(7123)
users = bot.serch_users(params)
   
    
photo_data=[]
final_list = bot.get_photos(users[2]["id"])
for list in final_list:
        photo_data.append({'id_vk': list['owner_id'],
                        'photo_id': list['id']})
def check_in():
        global unique_person_id, found_persons
        seen_person = []
        check_list=[]
        check_lst=photo_data
        for itm in check_lst:
             id_vk=itm['id_vk']
             check_list.append(id_vk)
             

        for i in check():  
            seen_person.append(i)
        if not seen_person:
            try:   
                unique_person_id = check_list
                return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons
        else:
            try:  
                for ifp in check_list:
                    if ifp in seen_person:
                        pass
                    else:
                        unique_person_id = ifp
                        return unique_person_id
            except NameError:
                found_persons = 0
                return found_persons

def ins_data():
        list_f=photo_data
        for ids in list_f:
                id_vk=ids['id_vk']
                insert_data_seen_person(id_vk)