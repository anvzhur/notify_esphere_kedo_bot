import asyncio
import datetime

from aiogram import Dispatcher
from aiogram.utils import executor

from handlers import DBCommands
from kedopack import kedolib
from load_all import dp
import config


async def display_date(loop, interval):
    end_time = loop.time() + 200.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(interval)


async def check_docs(dp: Dispatcher):
    from utils.sender import send_message_to_kdp
    dbc = DBCommands()
    max_event_id = await dbc.get_max_event_id()
    max_event_id = int(max_event_id)
    max_event_id += 1
    print(max_event_id)
    response = kedolib.get_event_list(max_event_id)
    print(response)
    events = response
    for ev in events:
        await dbc.add_event_id(ev["eventId"])
        if ev['objectType'] == 'Document':
            if ev['eventType'] == 'Create':
                docResponse = kedolib.getDoc(ev['objectId'])
                print(ev['objectId'])
                # print(docResponse)
                if docResponse == None:
                    continue
                urlpath = f"{config.URLPLATFORM}/documents?documentId={ev['objectId']}"
                out_text = f"Новый документ: {docResponse['name']} \n" \
                           f"тип документа: {docResponse['typeName']}\n" \
                           f"от {docResponse['creatorName']} {docResponse['isOutgoing']}\n" \
                           f"{urlpath}"


                print(out_text)
                await send_message_to_kdp(dp, out_text)
                # if docResponse["isOutgoing"] == "False":
                #   await send_message_to_kdp(dp, out_text)
                signers = kedolib.getSigners(ev['objectId'])['value']['items']
                for signer in signers:
                    if signer["status"] == "No":
                        print(signer)
                        print(signer['userId'])
                        print(signer['signerName'])


async def all(dp):
    while True:
        await check_docs(dp)
        await asyncio.sleep(30)


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(all(dp))
    executor.start_polling(dp, loop=loop, on_startup=on_startup)
