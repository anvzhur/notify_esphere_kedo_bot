import asyncio

from aiogram import Dispatcher
from aiogram.utils import executor

import config
from handlers import DBCommands
from kedopack import kedolib
from load_all import dp


async def check_docs(dp: Dispatcher):
    from utils.sender import send_message_to_kdp, send_message_to
    dbc = DBCommands()
    max_event_id = await dbc.get_max_event_id()
    max_event_id = int(max_event_id)
    max_event_id += 1
    response = kedolib.get_event_list(max_event_id)
    events = response
    for ev in events:
        await dbc.add_event_id(ev["eventId"])
        if ev['objectType'] == 'Document':
            if ev['eventType'] == 'Create':
                doc_response = kedolib.getDoc(ev['objectId'])
                if doc_response is None:
                    continue
                urlpath = f"{config.URLPLATFORM}/documents?documentId={ev['objectId']}"
                out_text = f"Новый документ: {doc_response['name']} \n" \
                           f"тип документа: {doc_response['typeName']}\n" \
                           f"от {doc_response['creatorName']}\n" \
                           f"{urlpath}"

                if doc_response["isOutgoing"] is True:
                    signers = kedolib.getSigners(ev['objectId'])['value']['items']
                    for signer in signers:
                        if signer["status"] == "No":
                            chat_id = await dbc.select_chat_id(signer['userId'])
                            if chat_id is not None:
                                await send_message_to(dp, chat_id, 'Сотруднику: \n' + out_text)
                else:
                    await send_message_to_kdp(dp, 'Кадровику:\n' + out_text)


async def startall(dp):
    while True:
        await check_docs(dp)
        await asyncio.sleep(30)


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(startall(dp))
    executor.start_polling(dp, loop=loop, on_startup=on_startup)
