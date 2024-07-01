from database.db_connect import connect
from hashlib import sha256
from random import choice

class User:
    
    def __init__(self, login: str = None):
        self.login = login

    async def get(self):
        db, sql = await connect()

        await sql.execute("SELECT * FROM users WHERE login = ?", (self.login,))
        result = await sql.fetchone()

        await db.close()

        if result is None:
            return None
        else:
            return {
                'login': result[0],
                'password': result[1],
                'permission_group': result[2]
            }

    @staticmethod
    async def filter(*args, **kwargs):
        if not kwargs:
            print("User(filter) **kwargs is empty")
            return None 

        db, sql = await connect()

        key = next(iter(kwargs)) 
        value = kwargs[key]

        await sql.execute("SELECT FROM users WHERE :column = :value", {"column": key, "value": value})
        result = await sql.fetchone()

        await db.close()

        if result is not None:
            return User(login = result[0])  
        else:
            return None

    @staticmethod
    async def add(*args, **kwargs):
        if not kwargs:
            print("User(add) **kwargs is empty")
            return False
        
        try:
            login = kwargs['login']
            password = str(kwargs['password'])
            password = sha256(password.encode('utf-8')).hexdigest()
            permission_group = kwargs['permission_group']

            db, sql = await connect()

            await sql.execute("INSERT INTO users VALUES (?, ?, ?)", (login, password, permission_group,))

            await db.commit()
            await db.close()

            return True
        except Exception as E:
            print(f'User(add) Error: {E}')
            return False

    async def create_session(self):
        try:
            def generate_key():
                chars = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
                
                key = ""
                for i in range(24):
                    key += choice(chars)

                return str(key)

            key = generate_key()

            db, sql = await connect()
            json_user = await self.get()

            await sql.execute("INSERT INTO sessions VALUES (?, ?)", (json_user['login'], str(key),))

            await db.commit()
            await db.close()

            return key
        except Exception as E:
            print(f'User(create_session) Error: {E}')
            return False
        
    async def auth(self, password: str):
        get = await self.get()

        if str(get.get('password')) == sha256(password.encode('utf-8')).hexdigest():
            result = await self.create_session()
            return result
        else:
            return False
        
    @staticmethod
    async def get_by_session(key: str):
        try:
            db, sql = await connect()

            await sql.execute("SELECT * FROM sessions WHERE session_key = ?", (key,))
            result = await sql.fetchone()

            await db.close()

            if result is None:
                return None
            else:
                return User(login = str(result[0]))
        except Exception as E:
            print(f'User(get_by_session) Error: {E}')
            return False
        
    async def set_admin(self):
        db, sql = await connect()

        await sql.execute("UPDATE users SET permission_group = 'ADMIN' WHERE login = ?", (self.login,))
        
        await db.commit()
        await db.close()

class Post:

    def __init__(self, post_id: int = None):
        self.post_id = post_id

    @staticmethod
    async def add(id: int, description: str, media: str, pub_date: str, forwards: int, views: int):
        if str(media).lower() in ['', 'None']:
            media = None
        
        db, sql = await connect()

        await sql.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)", (id, description, media, pub_date, forwards, views,))

        await db.commit()
        await db.close()

        return True

    @staticmethod
    async def get_all() -> list[dict]:
        db, sql = await connect()

        await sql.execute("SELECT * FROM posts")
        result = await sql.fetchall()

        await db.close()

        if result is None:
            return 
        
        return [
            {
                'id': post[0],
                'description': post[1],
                'media': post[2],
                'pub_date': post[3],
                'forwards': post[4],
                'views': post[5]
            } for post in result
        ]
    
    async def delete(self):
        db, sql = await connect()

        await sql.execute("DELETE FROM posts WHERE post_id = ?", (self.post_id,))
        
        await db.commit()
        await db.close()

        return True





    
