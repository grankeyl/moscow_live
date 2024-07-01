import aiosqlite

async def connect():
    db = await aiosqlite.connect('database/base.db')
    sql = await db.cursor()

    return db, sql 

async def create_tables():
    db, sql = await connect()

    await sql.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT,
        password TEXT,
        permission_group TEXT
    )""")

    await sql.execute("""CREATE TABLE IF NOT EXISTS sessions (
        login TEXT,
        session_key TEXT
    )""")

    await sql.execute("""CREATE TABLE IF NOT EXISTS posts (
        post_id INTEGER,
        description TEXT,
        media TEXT,
        pub_date TEXT,
        forwards INTEGER,
        views INTEGER
    )""")

    await db.commit()
    await db.close()
    