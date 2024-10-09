# from config import API_URL
import requests, re
from dt_baza import ReadDb


def Read_User(group):
    try:
        response = requests.get(group).json()
        ids = []
        for i in response:
            ids.append(i['id']) 
        
        max_id = max(ids)
        return max_id    
    except:
        return False
    

def IsFamiliy(familiya):
    pattern = r'^[A-ZА-Я][a-zа-я]*(ov|ev|ova|eva) [A-ZА-Я][a-zа-я]+$'
    return re.fullmatch(pattern, familiya) is not None


def TelefonCheck(tel):
    check = r"^([0-9][012345789]|[0-9][125679]|7[01234569])[0-9]{7}$"
    return re.match(check, tel) is not None


def BirthCheck(date):
    check = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19[0-9]{2}|20[0-9]{2})$"
    return re.match(check, date) is not None
