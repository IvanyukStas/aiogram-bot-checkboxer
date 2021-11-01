import aiosqlite, logging


class Aiosqlite_worker:

    async def create_database(self):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users(
                           userid INT PRIMARY KEY,
                           uname TEXT,
                           tg_id TEXT,
                           checkboxer_id INTEGER NOT NULL,
                           FOREIGN KEY (checkboxer_id) REFERENCES checkboxer(id));
                        """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkboxer(
                                       id INT PRIMARY KEY,
                                       chb_title TEXT,
                                       chb_status BOOL,
                                       checkbox_id INT,
                                       FOREIGN KEY (checkbox_id) REFERENCES checkbox(id));
                                    """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkbox(
                                                   id INT PRIMARY KEY,
                                                   chbox_title TEXT,
                                                   chb_status BOOL);
                                                """)
            await db.commit()
            logging.info('Создаем базу')
