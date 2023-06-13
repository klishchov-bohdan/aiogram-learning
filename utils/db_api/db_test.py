import asyncio

from data import config
from utils.db_api import quick_commands as qc
from utils.db_api.db_gino import db


async def db_test():
    await db.set_bind(config.POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await qc.add_user(1, 'limbo1', 'none')
    await qc.add_user(2, 'limbo2', 'uname2')
    await qc.add_user(3, 'limbo3', 'none')
    await qc.add_user(4, 'limbo4', 'none')

    users = await qc.select_all_users()
    print(users)

    count = await qc.count_users()
    print(count)

    user = await qc.select_user(2)
    print(user)

    await qc.update_user_name(1, 'new name')
    user = await qc.select_user(1)
    print(user)


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
