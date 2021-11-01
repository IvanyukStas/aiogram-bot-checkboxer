import aiosqlite


class Aiosqlite_worker:

    async def create_database(self):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users(
                           userid INT PRIMARY KEY,
                           fname TEXT,
                           lname TEXT,
                           gender TEXT);
                        """)
            await db.commit()

