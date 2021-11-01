import aiosqlite, logging


class Aiosqlite_worker:

    async def create_database(self):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           uname TEXT,
                           tg_id TEXT
                           );
                        """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkboxer(
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       chboxer_title TEXT,
                                       chboxer_status TEXT,
                                       user_id INT,
                                       FOREIGN KEY (user_id) REFERENCES user(id) 
                                       ON DELETE CASCADE)   ;                                       
                                    """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkbox(
                                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                   chbox_title TEXT,
                                                   chb_status BOOL,
                                                   checkboxer_id INT,
                                                   FOREIGN KEY (checkboxer_id) REFERENCES checkboxer(id)
                                                   ON DELETE CASCADE);
                                                """)
            await db.commit()
            logging.info('Создаем базу')


    async def add_new_user(self, user_name, tg_id):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute('INSERT INTO users(uname, tg_id) VALUES (?,?)', (user_name, tg_id))
            await db.commit()
            logging.info('Добавили нового пользователя!')


    async def add_new_checkboxer(self, chboxer_title, chboxer_status, user_id):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute('INSERT INTO checkboxer(chboxer_title, chboxer_status, user_id) VALUES (?,?,?)',(
                chboxer_title, chboxer_status, user_id))
            await db.commit()
            logging.info('Добавили новый чек боксер!')


    async def add_new_checkbox(self, chbox_title, chb_status, checkboxer_id):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute('INSERT INTO checkbox(chbox_title, chb_status,checkboxer_id) VALUES (?,?,?)',(
                chbox_title, chb_status, checkboxer_id))
            await db.commit()
            logging.info('Добавили новый чек бокс!')


    async def get_user(self, tg_id):
        async with aiosqlite.connect('aiodb.db') as db:
            await db.execute('SELECT id FROM users WHERE tg_id=?', tg_id)
            await db.commit()
        logging.info('Достаем пользователя')