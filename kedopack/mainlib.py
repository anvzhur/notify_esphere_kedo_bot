from kedopack import kedolib


def get_usr_id(snils):
    response = kedolib.getUsers()
    flag = 0
    for person in response['value']['items']:
        if person["snils"] == snils:
            flag = 1
            break
    if flag == 1:
        answer = person["userId"]
    else:
        answer = ''
    return answer


def get_updates():
    events = kedolib.get_event_list()


def prepare_send_list():
    pass


if __name__ == '__main__':
    get_usr_id("45290465794")
    get_usr_id("359099419342")
