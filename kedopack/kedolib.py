import requests

from config import KEDO_API_KEY_ADM, KEDO_API_KEY_KDP, URLPLATFORM


def get_event_list(event_id=0):
    url = f"{URLPLATFORM}/api/v1.0/manager/event?take=50&eventIdFrom={event_id}"
    headers = {
        'ApiKey': KEDO_API_KEY_ADM
    }
    response = requests.request("GET", url, headers=headers)

    return response.json()["value"]["items"]


def getDoc(docId):
    url = f"{URLPLATFORM}/api/v1.0/manager/document/{docId}"

    payload = {}
    headers = {
        'ApiKey': KEDO_API_KEY_KDP
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()["value"]
    else:
        return None


def getSigners(docId):
    url = f"{URLPLATFORM}/api/v1.0/signature?documentId={docId}"

    headers = {
        'ApiKey': KEDO_API_KEY_KDP
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()


def getUsers():
    url = f"{URLPLATFORM}/api/v1.0/manager/organizationUser"

    headers = {
        'ApiKey': KEDO_API_KEY_KDP
    }

    response = requests.request("GET", url, headers=headers)

    return response.json()
