import os
import psycopg2

from point import Point
from distance import get_distance

class Storage:

    def __init__(self, url):
        self.db_url = url

    def open(self):
        self.conn = psycopg2.connect(self.db_url, sslmode='require')
        self.cur = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_table(self):
        if self.db_url:
            self.open()
            self.cur.execute("CREATE TABLE IF NOT EXISTS test (id serial primary key, \
                user_id integer not null, info text not null, \
                location point, image bytea);")
            self.close()
        else:
            self.items = [
                [1, 1054860645, 'Кафешка на Московском', '(59.895913, 30.309837)', 'photos/1054860645_1.jpg'],
                [2, 1054860645, 'Ресторанчик где-то в переулке', '(59.896821, 30.301061)', 'photos/1054860645_2.jpg'],
                [3, 1054860645, 'Бар, Ближняя рогатка', '(59.895913, 30.310837)', 'photos/1054860645_3.jpg'],
                [4, 1054860645, 'Банк', '(59.894476, 30.302668)', 'photos/1054860645_4.jpg']
            ]
            # https://yandex.ru/maps/2/saint-petersburg/?ll=30.305753%2C59.895640&mode=routes&rtext=59.895913%2C30.309837~59.896821%2C30.301061~59.895913%2C30.310837~59.894476%2C30.302668&rtt=pd&ruri=~~~&z=16

    def save_item(self, user_id, info, location=None, image=None):
        if self.db_url:
            self.open()
            point = Point(*location) if location else None
            self.cur.execute(
                "INSERT INTO test (user_id, info, location, image) \
                    VALUES (%s, %s, %s, %s)",
                (user_id, info, point, image))
            self.close()
        else:
            item_id = len(self.items) + 1
            point = str(location) if location else None
            file_name = None
            if image:
                file_name = f'photos/{user_id}_{item_id}.jpg'
                with open(file_name, 'wb') as f:
                    f.write(image)
            self.items.append(
                [item_id, user_id, info, point, file_name])

    def get_all(self, user_id):
        if self.db_url:
            self.open()
            self.cur.execute(
                "SELECT * FROM test WHERE user_id = %s;",
                (user_id,))
            items = self.cur.fetchall()
            self.close()
        else:
            items = self.items

        return items

    def get_item(self, user_id):
        if self.db_url:
            self.open()
            self.cur.execute(
                "SELECT * FROM test WHERE user_id = %s ORDER BY id DESC LIMIT 1;",
                (user_id,))
            item = self.cur.fetchone()
            self.close()
        else:
            if self.items:
                item = self.items[-1].copy()
                if item[4]:
                    with open(item[4], 'rb') as f:
                        item[4] = f.read()
            else:
                item = None
        return item

    def get_nearby_items(self, user_id, point, R=0.5):
        items = self.get_all(user_id)
        nearby_items = []
        for item in items:
            if not item[3]:
                continue
            lat, lon = [float(c.strip()) for c in item[3][1:-1].split(',')]
            if get_distance(lat, lon, *point) <= R:
                nearby_items.append(item)
        return nearby_items

    def reset(self, user_id):
        if self.db_url:
            self.open()
            self.cur.execute("DELETE FROM test WHERE user_id = %s;", (user_id,))
            self.close()
        else:
            self.items = []
