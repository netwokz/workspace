from datetime import date, timedelta
from dotenv import dotenv_values


config = dotenv_values(
    "C:\\Users\\deanejst\\Documents\\CODE\\workspace\\temp\\.env")

# print(config.get('username'), config.get('password'))


dt = date.today()


def get_front_half_days(today):
    if today.weekday() == 6:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    elif today.weekday() == 0:
        start_of_week = today + timedelta(days=2)
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    elif today.weekday() == 1:
        start_of_week = today + timedelta(days=1)
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    else:
        start_of_week = today
        end_of_week = today + timedelta(days=(5 - today.weekday()))
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
    return start, end


def get_back_half_days(today):
    if today.weekday() == 0:
        start_of_week = today
        end_of_week = today + timedelta(days=2)
    elif today.weekday() == 1:
        start_of_week = today
        end_of_week = today + timedelta(days=1)
    elif today.weekday() == 2:
        start_of_week = today + timedelta(days=4)
        end_of_week = today + timedelta(days=7)
    elif today.weekday() == 3:
        start_of_week = today + timedelta(days=3)
        end_of_week = today + timedelta(days=6)
    elif today.weekday() == 4:
        start_of_week = today + timedelta(days=2)
        end_of_week = today + timedelta(days=5)
    elif today.weekday() == 5:
        start_of_week = today + timedelta(days=1)
        end_of_week = today + timedelta(days=4)
    elif today.weekday() == 6:
        start_of_week = today
        end_of_week = today + timedelta(days=3)
    start = start_of_week.strftime('%Y-%m-%d')
    end = end_of_week.strftime('%Y-%m-%d')
    return start, end


FHD_TECHS = ['ASHPFAF', 'GSALAEDW', 'IXTAJ', 'HERTAJU',
             'KIECLAR', 'WINNEMIC', 'HRYATAYL', 'CLARKSSI', 'FETICHER']

FHN_TECHS = ['CANDRUEL', 'QMOYCHRI', 'JOPADEYI', 'WLNJON',
             'JCSTROZ', 'MPEREZF', 'SHATPRAT', 'STUARTYL']

BHD_TECHS = ['AREAARON', 'VANBUC', 'ZDHARR', 'FELSOLON', 'ISAIACON',
             'JSONHU', 'JRRYCH', 'KKAMERJO', 'ANTOPLAC', 'LITTREDE']

BHN_TECHS = ['ADELALBA', 'AUSNMAJO', 'BUTLEEBR', 'RMGAB',
             'ACASJACO', 'REYESBJU', 'NATENEAL', 'JOVEROTL']


# def all_upper(my_list):
#     return [x.upper() for x in my_list]
# print(all_upper(BHN_TECHS))
