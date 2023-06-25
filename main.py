import psycopg2
from pprint import pprint

# СОЗДАНИЕ БД
#
# def create_db():
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#             # cur.execute("""
#             # DROP TABLE client CASCADE;
#             # DROP TABLE phone_numbers CASCADE;
#             # DROP TABLE e_mails CASCADE;
#             # """)
#             cur.execute("""
#             CREATE TABLE IF NOT EXISTS client(
#                 client_id SERIAL UNIQUE,
#                 first_name VARCHAR(40) NOT NULL,
#                 last_name VARCHAR(40) NOT NULL
#             );
#             """)
#             cur.execute("""
#             CREATE TABLE IF NOT EXISTS phone_numbers(
#                 client_id int REFERENCES client(client_id),
#                 phone_number NUMERIC
#             );
#             """)
#             cur.execute("""
#             CREATE TABLE IF NOT EXISTS e_mails(
#                 client_id int REFERENCES client(client_id),
#                 e_mail VARCHAR(60)
#             );
#             """)
#             conn.commit()
#     conn.close()
#
# create_db()


# ДОБАВЛЕНИЕ НОВОГО КЛИЕНТА

# def add_client(first_name, last_name, client_e_mails=None, client_phones = None):
#     if first_name is None or first_name == '' or first_name == ' ' or last_name is None or last_name == '' or last_name == ' ':
#         print('Client should have first name and last name together.')
#         return
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#
# # ВЫВОД ВСЕЙ ШНФОРМАЦИИ ИЗ ТАБЛИЦЫ CLIENT
#             cur.execute("""
#             SELECT *
#                 FROM client c
#                 WHERE first_name = %s and last_name = %s;
#             """, (first_name.capitalize(), last_name.capitalize()))
#             client_info = cur.fetchone()
#             # print(f' 1 client_info {client_info}')
#
# # ЕСЛИ ПОЛУЧЕННЫЕ ДАННЫЕ = None, ДОБАВЛЕНИЕ КЛИЕНТА В ТАБЛИЦУ CLIENT
#             if client_info is None:
#                 cur.execute("""
#                 INSERT INTO client(first_name, last_name)
#                     VALUES (%s, %s);
#                 """, (first_name.capitalize(), last_name.capitalize()))
#                 conn.commit()
#
# # ПОЛУЧЕНИЕ ID ДОБАВЛЕННОГО КЛИЕНТА
#                 cur.execute("""
#                 SELECT *
#                     FROM client
#                     WHERE first_name = %s and last_name = %s;
#                 """, (first_name.capitalize(), last_name.capitalize()))
#                 client_info = cur.fetchone()
#                 # print(f' 2 client_info {client_info}')
#
#                 client_id = client_info[0]
#
#                 print(f'Client {first_name.capitalize()} {last_name.capitalize()} added to data base, it\'s id - "{client_id}"')
#
# # ЕСЛИ ЗАДАНЫ НОМЕРА ТЕЛЕФОНА КЛИЕНТА, ДОБАВЛЕНИЕ В БД
#                 if len(client_phones) != 0:
#                     for i in client_phones:
#                         if len(str(i)) != 10:
#                             print(f'Phone number "{i}" should consists of ten digits.')
#                         else:
#                             cur.execute("""
#                             INSERT INTO phone_numbers(client_id, phone_number)
#                                 VALUES (%s, %s);
#                             """, (client_id, i))
#                             print(f'Client\'s {first_name.capitalize()} {last_name.capitalize()} phone number "{i}" added to phone_numbers table')
#                 elif len(client_phones) == 0:
#                     cur.execute("""
#                     INSERT INTO phone_numbers(client_id, phone_number)
#                         VALUES (%s, NULL);
#                     """, (client_id, ))
#
# # ЕСЛИ ЗАДАНЫ ЭЛЕКТРОННЫЕ АДРЕСА КЛИЕНТА, ДОБАВЛЕНИЕ В БД
#                 if len(client_e_mails) != 0:
#                     for i in client_e_mails:
#                         cur.execute("""
#                         INSERT INTO e_mails(client_id, e_mail)
#                             VALUES (%s, %s);
#                         """, (client_id, i))
#                     print(f'Client\'s {first_name.capitalize()} {last_name.capitalize()} e-mail(s) added to e_mails table')
#                 elif len(client_e_mails) == 0:
#                     cur.execute("""
#                     INSERT INTO e_mails(client_id, e_mail)
#                         VALUES (%s, NULL);
#                     """, (client_id, ))
#
# # ЕСЛИ ПОЛУЧЕННЫЕ ДАННЫЕ != 0...
#             elif client_info is not None:
#                 print(f'Client {first_name.capitalize()} {last_name.capitalize()} id "{client_info[0]}" already in data base.')
#
#                 cur.execute("""
#                 SELECT *
#                     FROM client
#                     WHERE first_name = %s and last_name = %s;
#                 """, (first_name.capitalize(), last_name.capitalize()))
#                 client_info = cur.fetchone()
#                 # print(f' 3 client_info {client_info}')
#
#                 client_id = client_info[0]
#
# # ЕСЛИ ЗАДАНЫ НОМЕРА ТЕЛЕФОНОВ, ДОБАВЛЕНИЕ В БД
#                 if client_phones:
#                     cur.execute("""
#                     SELECT *
#                         FROM phone_numbers
#                         WHERE client_id = %s;
#                     """, (client_id, ))
#                     client_info = cur.fetchall()
#                     # print(f' 4 client_info {client_info}')
#                     client_phone_numbers = []
#                     for i in client_info:
#                         if i[1] is None:
#                             cur.execute("""
#                             DELETE FROM phone_numbers
#                             WHERE phone_number is NULL;""")
#                         if i[1] is not None:
#                             client_phone_numbers.append(int(i[1]))
#                     for i in client_phones:
#                         if len(str(i)) == 10:
#                             if i in client_phone_numbers:
#                                 print(f'"{i}" already in phone_numbers table')
#                             else:
#                                 cur.execute("""
#                                 INSERT INTO phone_numbers(client_id, phone_number)
#                                     VALUES (%s, %s);
#                                 """, (client_id, i))
#                                 print(f'Client\'s {first_name.capitalize()} {last_name.capitalize()} phone number {i} added to phone_numbers_table')
#                         else:
#                             print(f'Phone number "{i}" should consists of ten digits.')
#
# # ЕСЛИ ЗАДАНЫ ЭЛ. АДРЕСА, ДОБАВЛЕНИЕ В БД
#                 if client_e_mails:
#                     cur.execute("""
#                     SELECT *
#                         FROM e_mails
#                         WHERE client_id = %s;
#                     """, (client_id,))
#                     client_info = cur.fetchall()
#                     # print(f' 5 e-mail client_info {client_info}')
#                     e_mails = []
#                     for i in client_info:
#                         if i[1] is None:
#                             cur.execute("""
#                             DELETE FROM e_mails
#                             WHERE e_mail is NULL;""")
#                         e_mails.append(i[1])
#                     for i in client_e_mails:
#                         if i in e_mails:
#                             print(f'{i} already in e_mails table')
#                         else:
#                             cur.execute("""
#                             INSERT INTO e_mails(client_id, e_mail)
#                                 VALUES (%s, %s);
#                             """, (client_id, i))
#                             print(f'Client\'s {first_name.capitalize()} {last_name.capitalize()} e-mail {i} added to e_mails table')
#
#
#             conn.commit()
#     conn.close()
#
# client_phones = [7777777777, 8888888888]
# client_e_mails = []
# first_name = 'alan'
# last_name = 'ivanov'
#
# add_client(first_name, last_name, client_e_mails, client_phones)


# ДОБАВЛЕНИЕ НОМЕРА ТЕЛЕФОНА ДЛЯ СУЩЕСТВУЮЩЕГО КЛИЕНТА

# def add_phone(client_id, phones):
#
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#             SELECT c.client_id, first_name, last_name, phone_number
#             FROM client c
#             JOIN phone_numbers pn on c.client_id = pn.client_id
#             WHERE pn.client_id = %s;
#             """, (client_id, ))
#             client_info = cur.fetchall()
#             print(client_info)
#             if len(client_info) == 0:
#                 print(f'No client under id №{client_id} in database.')
#                 return
#             elif len(client_info) != 0:
#                 client_phone_numbers = []
#                 for i in client_info:
#                     client_phone_numbers.append(int(i[3]))
#                 for i in phones:
#                     if len(str(i)) != 10:
#                         print(f'Wrong "{i}" phone number format. Must be ten digits.')
#                     else:
#                         if i in client_phone_numbers:
#                             print(f'Client {client_info[0][1]} {client_info[0][2]} already has "{i}" phone number.')
#                         else:
#                             cur.execute("""
#                             INSERT INTO phone_numbers(client_id, phone_number) VALUES(%s, %s);
#                             """, (client_id, i))
#                             conn.commit()
#                             print(f'Now client {client_info[0][1]} {client_info[0][2]} has "{i}" phone number.')
#             conn.commit()
#     conn.close()
#
# phones = [1111111111, 1234567890, 888888888888879]
#
# add_phone(1, phones)


# ИЗМЕНЕНЕИЕ ДАННЫХ О КЛИЕНТЕ

# def change_client(client_id, first_name=None, last_name=None, emails=None, phones=None):
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#             if first_name is None or first_name == '' or first_name == ' ' or last_name is None or last_name == '' or last_name == ' ':
#                 print('Client should have name and last name.')
#                 return
#             elif first_name is not None and last_name is not None:
#                 cur.execute("""
#                 SELECT client_id, first_name, last_name
#                 FROM client
#                 WHERE (client_id = %s);
#                 """, (client_id,))
#                 client_fn_ln = cur.fetchall()
#                 # print(f'client_info \n{client_fn_ln}')
#                 if client_fn_ln:
#                     if first_name.capitalize() == client_fn_ln[0][1] and last_name.capitalize() == client_fn_ln[0][2]:
#                         print(f'Client {first_name.capitalize()} {last_name.capitalize()} already under id №{client_id}.')
#                     else:
#                         cur.execute("""
#                         UPDATE client SET (first_name, last_name) = (%s, %s)
#                         WHERE client_id = %s;
#                         """, (first_name.capitalize(), last_name.capitalize(), client_id))
#                         print(f'Now {first_name.capitalize()} {last_name.capitalize()} updated to client table under id №{client_id} ')
#                     if emails is not None:
#                         cur.execute("""
#                         DELETE FROM e_mails WHERE client_id=%s;
#                         """, (client_id,))
#                         for i in emails:
#                             cur.execute("""
#                             INSERT INTO e_mails (client_id, e_mail)
#                                 VALUES (%s, %s)
#                                 """, (client_id, i))
#                             print(f'Now {first_name.capitalize()} {last_name.capitalize()} e-mail "{i}" in e_mails table.')
#                     if phones is not None:
#                         cur.execute("""
#                         DELETE FROM phone_numbers WHERE client_id=%s;
#                         """, (client_id,))
#                         for i in phones:
#                             if len(str(i)) != 10:
#                                 print(f'Wrong "{i}" phone number format. Must be ten digits.')
#                             else:
#                                 cur.execute("""
#                                 INSERT INTO phone_numbers (client_id, phone_number)
#                                     VALUES (%s, %s)
#                                     """, (client_id, i))
#                                 print(f'Now {first_name.capitalize()} {last_name.capitalize()} phone number "{i}" in phone-numbers table.')
#                 else:
#                     print(f'No client under id №{client_id} in data base')
#             conn.commit()
#     conn.close()
#
# client_phones = [9600719526, 9274882303, 9600719525, 9967233557, 9653214576, 9653214577]
# client_e_mails = ['alan.zybtsev@mail.ru', 'alfira.zybtseva@mail.ru']
#
# change_client(client_id=2, first_name='gul', last_name='val', emails=client_e_mails, phones=client_phones)


# УДАЛЕНИЕ ТЕЛЕФОНА ДЛЯ СУЩЕСТВУЮЩЕГО КЛИЕНТА
#
# def delete_phone(client_id, phones):
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#             SELECT *
#                 FROM phone_numbers
#                 WHERE (client_id = %s);
#             """, (client_id,))
#             client_id_phones = cur.fetchall()
#             # print(client_id_phones)
#             client_phones = []
#             if client_id_phones:
#                 for i in client_id_phones:
#                     client_phones.append(int(i[1]))
#                     for n in phones:
#                         if int(i[1]) == n:
#                             cur.execute("""
#                             DELETE FROM phone_numbers WHERE phone_number=%s;
#                             """, (n,))
#                             print(f'Phone number "{n}" removed from phone_numbers table.')
#                 # print(client_phones)
#                 for i in phones:
#                     if i not in client_phones:
#                         print(f'No phone number "{i}" under id №{client_id} in phone_numbers table')
#             else:
#                 print(f'No client under id №{client_id} in data base')
#         conn.commit()
#     conn.close()
#
# phones = [9600719526, 9274882303, 9600719525, 9967233557, 7777777777]
#
# delete_phone(2, phones)

#
# УДАЛЕНИЕ СУЩЕСТВУЮЩЕГО КЛИЕНТА

# def delete_client(client_id):
#     with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
#         with conn.cursor() as cur:
#             for i in client_id:
#                 cur.execute("""
#                 SELECT *
#                     FROM client
#                     WHERE client_id = %s;
#                 """, (i, ))
#                 client_info = cur.fetchall()
#                 print(f'{client_info}')
#                 if len(client_info) != 0:
#                     cur.execute("""
#                     DELETE FROM phone_numbers WHERE client_id=%s;
#                     """, (i,))
#                     conn.commit()
#                     print(f'\nPhone numbers under id №{i} removed from phone_numbers table.')
#                     cur.execute("""
#                     DELETE FROM e_mails WHERE client_id=%s;
#                     """, (i,))
#                     conn.commit()
#                     print(f'E-mails under id №{i} removed from e_mails table.')
#                     cur.execute("""
#                     DELETE FROM client WHERE client_id=%s;
#                     """, (i,))
#                     conn.commit()
#                     print(f'Client under id №{i} removed from client table.\n')
#                 else:
#                     print(f'There is no client under {i} in data base\n')
#             conn.commit()
#     conn.close()
#
# client_id = [2, 3]
#
# delete_client(client_id)


# НАЙТИ КЛИЕНТА ПО ЕГО ДАННЫМ: имени, фамилии, email или телефону

def find_client(first_name=None, last_name=None, email=None, phone=None):
    with psycopg2.connect(database="netology_db", user="postgres", password="EkbwfHfcrjkmybrjdf9)") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
            FROM client c
            JOIN phone_numbers pn ON c.client_id = pn.client_id
            JOIN e_mails em ON c.client_id = em.client_id
            WHERE c.first_name = %s AND c.last_name = %s;
            """, (first_name, last_name))
            client_info = cur.fetchall()
            # pprint(client_info)
            first_name_last_name = []
            if first_name and last_name:
                cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
                    FROM client c
                    JOIN phone_numbers pn ON c.client_id = pn.client_id
                    JOIN e_mails em ON c.client_id = em.client_id
                    WHERE c.first_name = %s AND c.last_name = %s;
                """, (first_name.capitalize(), last_name.capitalize()))
                client_info = cur.fetchall()
                pprint(client_info)
            elif first_name:
                cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
                    FROM client c
                    JOIN phone_numbers pn ON c.client_id = pn.client_id
                    JOIN e_mails em ON c.client_id = em.client_id
                    WHERE c.first_name = %s;
                """, (first_name.capitalize(),))
                client_info = cur.fetchall()
                pprint(client_info)
            elif last_name:
                cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
                    FROM client c
                    JOIN phone_numbers pn ON c.client_id = pn.client_id
                    JOIN e_mails em ON c.client_id = em.client_id
                    WHERE c.last_name = %s;
                """, (last_name.capitalize(),))
                client_info = cur.fetchall()
                pprint(client_info)
            elif email:
                cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
                    FROM client c
                    JOIN phone_numbers pn ON c.client_id = pn.client_id
                    JOIN e_mails em ON c.client_id = em.client_id
                    WHERE em.e_mail = %s;
                """, (email,))
                client_info = cur.fetchall()
                pprint(client_info)
            elif phone:
                cur.execute("""
                SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
                    FROM client c
                    JOIN phone_numbers pn ON c.client_id = pn.client_id
                    JOIN e_mails em ON c.client_id = em.client_id
                    WHERE pn.phone_number = %s;
                """, (phone,))
                client_info = cur.fetchall()
                pprint(client_info)
            conn.commit()
    conn.close()

# first_name = 'alan'
# last_name = 'zybtsev'
# email = 'alan.zybtsev@gmail.com'
phone = 1111111111

find_client(phone=phone)

with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    pass
conn.close()
