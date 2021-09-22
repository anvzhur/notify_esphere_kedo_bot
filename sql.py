import asyncio
import logging

import asyncpg

from config import host, PG_USER, PG_PASS, PG_DATABASE

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def create_db():
    create_db_command = open("create_db.sql", "r").read()

    logging.info(f"Connecting to database...{PG_DATABASE}")
    try:
        conn: asyncpg.Connection = await asyncpg.connect(user=PG_USER,
                                                         password=PG_PASS,
                                                         host=host,
                                                         database=PG_DATABASE)
    except:
        # Database does not exist, create it.
        sys_conn: asyncpg.Connection = await asyncpg.connect(user=PG_USER,
                                                             password=PG_PASS,
                                                             host=host)
        await sys_conn.execute(
            f'CREATE DATABASE "{PG_DATABASE}" OWNER "{PG_USER}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        conn: asyncpg.Connection = await asyncpg.connect(user=PG_USER,
                                                         password=PG_PASS,
                                                         host=host,
                                                         database=PG_DATABASE)
    await conn.execute(create_db_command)
    await conn.close()
    logging.info("Table users created")


async def create_pool():
    return await asyncpg.create_pool(user=PG_USER,
                                     password=PG_PASS,
                                     host=host,
                                     database=PG_DATABASE)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
