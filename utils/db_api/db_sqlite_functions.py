import sqlite3
import aiosqlite, logging


class Aiosqlite_worker:

    def __init__(self, db_name='aiodb.db') -> None:
        self.db_name: str = db_name

    async def create_database_sqlite(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS users(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           uname TEXT,
                           tg_id TEXT UNIQUE 
                           );
                        """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkboxers(
                                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       chboxer_title TEXT,
                                       chboxer_status TEXT,
                                       tg_id TEXT ,
                                       FOREIGN KEY (tg_id) REFERENCES user(tg_id) 
                                       ON DELETE CASCADE)   ;                                       
                                    """)
            await db.execute("""CREATE TABLE IF NOT EXISTS checkbox(
                                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                   chbox_title TEXT,
                                                   chb_status TEXT,
                                                   checkboxer_id INT,
                                                   FOREIGN KEY (checkboxer_id) REFERENCES checkboxers(id)
                                                   ON DELETE CASCADE);
                                                """)
            await db.commit()
            logging.info('Создаем базу')


    async def add_new_user_sqlite(self, user_name, tg_id):
            try:
                async with aiosqlite.connect(self.db_name) as db:
                    await db.execute('INSERT INTO users(uname, tg_id) VALUES (?,?)', (user_name, tg_id))
                    await db.commit()
                    logging.info('Добавили нового пользователя!')
                return True
            except sqlite3.IntegrityError:
                return False


    async def add_new_checkboxer_sqlite(self, chboxer_title, tg_id, chboxer_status='private'):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT INTO checkboxers(chboxer_title, chboxer_status, tg_id) VALUES (?,?,?)',(
                chboxer_title, chboxer_status, tg_id))
            await db.commit()
            logging.info('Добавили новый чек боксер!')


    async def add_new_checkbox_sqlite(self, chbox_title, checkboxer_id, chb_status=0):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT INTO checkbox(chbox_title, chb_status, checkboxer_id) VALUES (?,?,?)',(
                chbox_title, chb_status, checkboxer_id))
            await db.commit()
            logging.info('Добавили новый чек бокс!')


    async def get_user_sqlite(self, tg_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT id FROM users WHERE tg_id=?', (tg_id,))
            row = await cursor.fetchone()
        logging.info('Достаем пользователя')
        return row


    async def get_checkboxers_sqlite(self, tg_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT id, chboxer_title FROM checkboxers WHERE tg_id=?', (tg_id,))
            rows = await cursor.fetchall()
        logging.info('Достаем чекбоксеры юзера')
        return rows


    async def get_checkboxes_sqlite(self, checkboxer_id):
        async with aiosqlite.connect(self.db_name) as db:
            cursor = await db.execute('SELECT id, chbox_title, chb_status FROM checkbox '
                                      'WHERE checkboxer_id=?'
                                      'ORDER BY chb_status', (checkboxer_id,))
            rows = await cursor.fetchall()
        logging.info('Достаем чекбоксеры юзера')
        if len(rows) > 0:
            return rows
        else:
            return False


    async def update_checkbox_sqlite(self, id, status):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('UPDATE checkbox SET chb_status=? WHERE id=?', (status, id))
            await db.commit()
        logging.info(f'Обновили статус у чекбокса {id}')


    async def set_all_checkboxes_to_uncheck_sqlite(self, checkboxer_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(f'UPDATE checkbox SET chb_status=0 WHERE checkboxer_id={checkboxer_id}')
            await db.commit()
        logging.info('Используем set_all_checkboxes_to_uncheck')
