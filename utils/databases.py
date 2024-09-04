import aiosqlite

class VerifDataBase:
    def __init__(self):
        self.name = 'database/verif.db'

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS verif (
                target_user TEXT PRIMARY KEY,
                verificator TEXT NOT NULL,
                reason TEXT
            )'''
            await cursor.execute(query)
            await db.commit()

    async def add_verif_user(self, target_user: str, verificator: str, reason: str):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(target_user):
                cursor = await db.cursor()
                query = 'INSERT INTO verif (target_user, verificator, reason) VALUES (?, ?, ?)'
                await cursor.execute(query, (target_user, verificator, reason))
                await db.commit()

    async def get_user(self, target_user: str):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM verif WHERE target_user =?'
            await cursor.execute(query, (target_user,))
            return await cursor.fetchone()
