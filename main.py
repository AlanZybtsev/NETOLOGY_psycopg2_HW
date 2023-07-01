import psycopg2
from pprint import pprint

# СОЗДАНИЕ БД
def create_db(conn):

    # cur.execute("""
    # DROP TABLE client CASCADE;
    # DROP TABLE phone_numbers CASCADE;
    # DROP TABLE e_mails CASCADE;
    # """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
        client_id SERIAL UNIQUE,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_numbers(
        client_id int REFERENCES client(client_id),
        phone_number NUMERIC UNIQUE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS e_mails(
        client_id int REFERENCES client(client_id),
        e_mail VARCHAR(60)
    );
    """)
    print('Data base created.')
    conn.commit()

# ДОБАВЛЕНИЕ НОВОГО КЛИЕНТА
def add_client(conn, first_name, last_name, client_e_mails=None, client_phones = None):

# ВЫВОД ВСЕЙ ИНФОРМАЦИИ ИЗ ТАБЛИЦЫ CLIENT
    cur.execute("""
    SELECT *
        FROM client
        WHERE first_name = %s and last_name = %s;
    """, (first_name.capitalize(), last_name.capitalize()))
    client_info = cur.fetchone()
    # print(f' 1 client_info {client_info}')

# ЕСЛИ ПОЛУЧЕННЫЕ ДАННЫЕ = None, ДОБАВЛЕНИЕ КЛИЕНТА В ТАБЛИЦУ CLIENT
    if client_info is None:
        cur.execute("""
        INSERT INTO client(first_name, last_name)
            VALUES (%s, %s);
        """, (first_name.capitalize(), last_name.capitalize()))
        conn.commit()

# ПОЛУЧЕНИЕ ID ДОБАВЛЕННОГО КЛИЕНТА
        cur.execute("""
        SELECT *
            FROM client
            WHERE first_name = %s and last_name = %s;
        """, (first_name.capitalize(), last_name.capitalize()))
        client_info = cur.fetchone()
        # print(f' 2 client_info {client_info}')
        client_id = client_info[0]
        print(f'{first_name.capitalize()} {last_name.capitalize()} added to "client" table under id №{client_id}.')

# ЕСЛИ ЗАДАНЫ НОМЕРА ТЕЛЕФОНА КЛИЕНТА, ДОБАВЛЕНИЕ В БД
        if len(client_phones) != 0:
            print(f'client_id {client_id}')
            cur.execute("""
            SELECT phone_number
                FROM phone_numbers;
            """, )
            all_phones_from_bd = cur.fetchall()
            all_phones_from_bd_list = []
            for n in all_phones_from_bd:
                if n[0] is not None:
                    all_phones_from_bd_list.append(int(n[0]))
            for i in client_phones:
                if i in all_phones_from_bd_list:
                    print(f'Phone number "{i} can not be added to "phone_numbers" table because it is already there')
                else:
                    cur.execute("""
                    INSERT INTO phone_numbers(client_id, phone_number)
                        VALUES (%s, %s);
                    """, (client_id, i))
                    conn.commit()
                    print(f'Phone number "{i}" added to "phone_numbers" table under id №{client_id}.')

        elif len(client_phones) == 0:
            cur.execute("""
            INSERT INTO phone_numbers(client_id, phone_number)
                VALUES (%s, NULL);
            """, (client_id, ))
            conn.commit()

# ЕСЛИ ЗАДАНЫ ЭЛЕКТРОННЫЕ АДРЕСА КЛИЕНТА, ДОБАВЛЕНИЕ В БД
        for i in client_e_mails:
            cur.execute("""
            INSERT INTO e_mails(client_id, e_mail)
                VALUES (%s, %s);
            """, (client_id, i))
            conn.commit()
            print(f'E-mail "{i}" added to "e_mails" table under id №{client_id}.')


# ЕСЛИ ПОЛУЧЕННЫЕ ДАННЫЕ != 0...
    elif client_info is not None:
        print(f'{first_name.capitalize()} {last_name.capitalize()} already in "client" table under id №{client_info[0]}')

        cur.execute("""
        SELECT *
            FROM client
            WHERE first_name = %s and last_name = %s;
        """, (first_name.capitalize(), last_name.capitalize()))
        client_info = cur.fetchone()
        # print(f' 3 client_info {client_info}')

        client_id = client_info[0]

# ЕСЛИ ЗАДАНЫ НОМЕРА ТЕЛЕФОНОВ, ДОБАВЛЕНИЕ В БД
        if client_phones:

            cur.execute("""
            SELECT phone_number
               FROM phone_numbers;
           """)
            client_info = cur.fetchall()
            # print(f' 4 client_info {client_info}')
            db_phone_numbers = []
            for i in client_info:
                if i[0] is not None:
                    db_phone_numbers.append(int(i[0]))
            # print(f'db_phone_numbers {db_phone_numbers}')
            for i in client_phones:
                if i in db_phone_numbers:
                    print(f'Phone number "{i} can not be added to "phone_numbers" table because it is already there')
                elif i not in db_phone_numbers:

                    # for n in client_phones:
                    cur.execute("""
                    INSERT INTO phone_numbers(client_id, phone_number)
                        VALUES (%s, %s);
                    """, (client_id, i))
                    conn.commit()
                    print(f'Phone number "{i}" added to "phone_numbers" under id №{client_id}')

                cur.execute("""
                SELECT phone_number
                   FROM phone_numbers
                   WHERE client_id = %s;
                """, (client_id,))
                client_ph = cur.fetchall()
                for n in client_ph:
                    if n[0] is None:
                        cur.execute("""
                        DELETE FROM phone_numbers
                           WHERE phone_number is NULL AND client_id = %s;
                           """, (client_id,))
                        conn.commit()

# ЕСЛИ ЗАДАНЫ ЭЛ. АДРЕСА, ДОБАВЛЕНИЕ В БД
        if client_e_mails:
            cur.execute("""
            SELECT *
                FROM e_mails
                WHERE client_id = %s;
            """, (client_id,))
            client_info = cur.fetchall()
            # print(f' 5 e-mail client_info {client_info}')
            e_mails = []
            for i in client_info:
                if i[1] is None:
                    cur.execute("""
                    DELETE FROM e_mails
                    WHERE e_mail is NULL;""")
                    conn.commit()
                e_mails.append(i[1])
            for i in client_e_mails:
                if i in e_mails:
                    print(f'E-mail "{i}" already in "e_mails" table under id №{client_id}')
                else:
                    cur.execute("""
                    INSERT INTO e_mails(client_id, e_mail)
                        VALUES (%s, %s);
                    """, (client_id, i))
                    conn.commit()
                    print(f'E-mail "{i}" added to "e_mails" table under id №{client_id}')


# ДОБАВЛЕНИЕ НОМЕРА ТЕЛЕФОНА ДЛЯ СУЩЕСТВУЮЩЕГО КЛИЕНТA
def add_phone(conn, client_id, phones):
    cur.execute("""
                SELECT phone_number
                   FROM phone_numbers;
               """)
    client_info = cur.fetchall()
    # print(f' 4 client_info {client_info}')
    db_phone_numbers = []
    for i in client_info:
        if i[0] is not None:
            db_phone_numbers.append(int(i[0]))
    # print(f'db_phone_numbers {db_phone_numbers}')
    for i in phones:
        if i in db_phone_numbers:
            print(f'Phone number "{i} can not be added to "phone_numbers" table because it is already there')
        elif i not in db_phone_numbers:

            # for n in client_phones:
            cur.execute("""
                        INSERT INTO phone_numbers(client_id, phone_number)
                            VALUES (%s, %s);
                        """, (client_id, i))
            conn.commit()
            print(f'Phone number "{i}" added to "phone_numbers" under id №{client_id}')

        cur.execute("""
                    SELECT phone_number
                       FROM phone_numbers
                       WHERE client_id = %s;
                    """, (client_id,))
        client_ph = cur.fetchall()
        for n in client_ph:
            if n[0] is None:
                cur.execute("""
                            DELETE FROM phone_numbers
                               WHERE phone_number is NULL AND client_id = %s;
                               """, (client_id,))
                conn.commit()

# ИЗМЕНЕНЕИЕ ДАННЫХ О КЛИЕНТЕ
def change_client(conn, client_id, first_name, last_name, emails, phones):
    cur.execute("""
    SELECT client_id, first_name, last_name
        FROM client
        WHERE (client_id = %s);
    """, (client_id,))
    client_fn_ln = cur.fetchall()
    print(f'client_info \n{client_fn_ln}')

    if client_fn_ln:
        if first_name == '-':
            pass
        else:
            cur.execute("""
                UPDATE client SET first_name = %s
                WHERE client_id = %s;
            """, (first_name.capitalize(), client_id))
            conn.commit()
            print(f'Client under id №{client_id} first name changed to "{first_name.capitalize()}".')

        if last_name == '-':
            pass
        else:
            cur.execute("""
                UPDATE client SET last_name = %s
                WHERE client_id = %s;
            """, (last_name.capitalize(), client_id))
            conn.commit()
            print(f'Client under id №{client_id} last name changed to "{first_name.capitalize()}".')

        if len(emails) == 0:
            pass
        else:
            cur.execute("""
            DELETE FROM e_mails WHERE client_id = %s;
            """, (client_id,))
            conn.commit()
            for i in emails:
                cur.execute("""
                    INSERT INTO e_mails (client_id, e_mail) VALUES (%s, %s);
                """, (client_id, i))
                conn.commit()
                print(f'To client under id №{client_id} has been assigned "{i}" e-mail address.')

        if len(phones) == 0:
            pass
        else:
            cur.execute("""
            DELETE FROM phone_numbers WHERE client_id = %s;
            """, (client_id,))
            conn.commit()
            for i in phones:
                cur.execute("""
                    INSERT INTO phone_numbers (client_id, phone_number) VALUES (%s, %s);
                """, (client_id, i))
                conn.commit()
                print(f'To client under id №{client_id} has been assigned "{i}" phone number.')
    else:
        print(f'No client under id №{client_id} in data base')

# УДАЛЕНИЕ ТЕЛЕФОНА ДЛЯ СУЩЕСТВУЮЩЕГО КЛИЕНТА
def delete_phone(client_id):
            cur.execute("""
            SELECT *
                FROM phone_numbers
                WHERE (client_id = %s);
            """, (client_id,))
            client_id_phones = cur.fetchall()
            if len(client_id_phones) == 1:
                for i in client_id_phones:
                    if i[1] is None:
                        print(f'No phone numbers under id №{client_id} in "phone_numbers" table.')
                    else:
                        print(f'There is only "{i[1]}" phone number under id №{client_id} in "phone_numbers" table. '
                              f'\n\tDelete it? (+/-): ')
                        desicion = input()
                        yes_no = ['-', '+']
                        if desicion not in yes_no:
                            print('Choose "+" or "-".')
                        if desicion == '+':
                            print(f'Phone number "{i[1]}" under id №{client_id} removed from "phone_numbers" table.')
                            cur.execute("""
                                UPDATE phone_numbers SET phone_number = NULL
                                WHERE client_id = %s;
                            """, (client_id,))
                            conn.commit()
            elif len(client_id_phones) != 1:
                # print(f'client_id_phones {client_id_phones}')
                print('Select phone number(s) from the list below:')
                all_client_numbers = []
                for id, i in enumerate(client_id_phones, 1):
                    print(f'{id} - {int(i[1])}')
                    all_client_numbers.append(int(i[1]))
                numbers_to_delete_list = []
                while True:
                    delete_p_n = input()
                    if delete_p_n == '-':
                        break
                    try:
                        delete_p_n = int(delete_p_n)
                    except ValueError:
                        print('Wrong data format. Try again.')
                    else:
                        if delete_p_n > len(client_id_phones) or delete_p_n < 1:
                            print('Wrong number. Select from the list.')
                        elif int(client_id_phones[delete_p_n-1][1]) in numbers_to_delete_list:
                            print(f'Phone number "{int(client_id_phones[delete_p_n-1][1])}" already chosen".')
                        else:
                            numbers_to_delete_list.append(int(client_id_phones[delete_p_n-1][1]))
                for i in numbers_to_delete_list:
                    cur.execute("""
                        DELETE FROM phone_numbers WHERE client_id = %s AND phone_number = %s;
                        """, (client_id, i))
                    conn.commit()
                    all_client_numbers.remove(i)
                    if len(all_client_numbers) == 0:
                        cur.execute("""
                            INSERT INTO phone_numbers (client_id, phone_number) VALUES (%s, %s);
                        """, (client_id, None))
                        conn.commit()
                    print(f'Phone number "{i}" under id №{client_id} removed from "phone_numbers" table.')

# УДАЛЕНИЕ СУЩЕСТВУЮЩЕГО КЛИЕНТА
def delete_client(conn, client_id):
    # for i in client_id:
    cur.execute("""
    SELECT *
        FROM client
        WHERE client_id = %s;
    """, (client_id, ))
    client_info = cur.fetchall()
    # print(f'{client_info}')
    if len(client_info) != 0:
        cur.execute("""
        DELETE FROM phone_numbers WHERE client_id=%s;
        """, (client_id,))
        conn.commit()
        print(f'\nPhone numbers under id №{client_id} removed from "phone_numbers" table.')
        cur.execute("""
        DELETE FROM e_mails WHERE client_id=%s;
        """, (client_id,))
        conn.commit()
        print(f'E-mails under id №{client_id} removed from "e_mails" table.')
        cur.execute("""
        DELETE FROM client WHERE client_id=%s;
        """, (client_id,))
        conn.commit()
        print(f'Client under id №{client_id} removed from "client" table.\n')
    else:
        print(f'No client under id №{client_id} in data base\n')

# НАЙТИ КЛИЕНТА ПО ЕГО ДАННЫМ: имени, фамилии, email или телефону
def find_client(conn, first_name, last_name, email, phone):
    # print(first_name, last_name, email, phone)
    if first_name is not None and last_name is not None and email is not None:
        cur.execute("""
        SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
            FROM client c
            JOIN phone_numbers pn ON c.client_id = pn.client_id
            JOIN e_mails em ON c.client_id = em.client_id
            WHERE c.first_name = %s AND c.last_name = %s AND e_mail =%s;
        """, (first_name.capitalize(), last_name.capitalize(), email))
        client_info = cur.fetchall()
        if len(client_info) != 0:
            print(f'\nClients id - {client_info[0][0]} \nClients first name - {client_info[0][1]} \n'
                   f'Clients last name - {client_info[0][2]} \n')
            print(f'Client has phone numbers:')
            for i in client_info:
                print(i[3])
            id = client_info[0][0]
            cur.execute("""
            SELECT client_id, e_mail
                FROM e_mails
                WHERE client_id = %s;
            """, (id, ))
            client_e_m = cur.fetchall()
            print(f'\nClient has e-mails:')
            for i in client_e_m:
                print(i[1])
        else:
            print(f'Can not identify any client.')
    elif first_name is not None and last_name is not None:
        cur.execute("""
        SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
            FROM client c
            JOIN phone_numbers pn ON c.client_id = pn.client_id
            JOIN e_mails em ON c.client_id = em.client_id
            WHERE c.first_name = %s AND c.last_name = %s;
        """, (first_name.capitalize(), last_name.capitalize()))
        client_info = cur.fetchall()
        if len(client_info) != 0:
            print(f'\nClients id - {client_info[0][0]} \nClients first name - {client_info[0][1]} \n'
                  f'Clients last name - {client_info[0][2]} \n')
            client_id = client_info[0][0]
            cur.execute("""
            SELECT client_id, phone_number
                FROM phone_numbers
                WHERE client_id = %s;
            """, (client_id,))
            client_p_n = cur.fetchall()
            print(f'Client has phone numbers:')
            for i in client_p_n:
                print(i[1])
            cur.execute("""
            SELECT client_id, e_mail
                FROM e_mails
                WHERE client_id = %s;
            """, (client_id,))
            client_e_m = cur.fetchall()
            print(f'\nClient has e-mails:')
            for i in client_e_m:
                print(i[1])
        else:
            print(f'Can not identify any client.')

# elif first_name is not None:
#     cur.execute("""
    #     SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
    #         FROM client c
    #         JOIN phone_numbers pn ON c.client_id = pn.client_id
    #         JOIN e_mails em ON c.client_id = em.client_id
    #         WHERE c.first_name = %s;
    #     """, (first_name.capitalize(),))
    #     client_info = cur.fetchall()
    #     pprint(f'3 {client_info}')

    # elif last_name is not None:
    #     cur.execute("""
    #     SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
    #         FROM client c
    #         JOIN phone_numbers pn ON c.client_id = pn.client_id
    #         JOIN e_mails em ON c.client_id = em.client_id
    #         WHERE c.last_name = %s;
    #     """, (last_name.capitalize(),))
    #     client_info = cur.fetchall()
    #     print(4)
    #     pprint(client_info)

    # elif email is not None:
    #     cur.execute("""
    #     SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
    #         FROM client c
    #         JOIN phone_numbers pn ON c.client_id = pn.client_id
    #         JOIN e_mails em ON c.client_id = em.client_id
    #         WHERE em.e_mail = %s;
    #     """, (email,))
    #     client_info = cur.fetchall()
    #     pprint(f'5 {client_info}')

    elif phone is not None:
        cur.execute("""
        SELECT c.client_id, c.first_name, c.last_name, pn.phone_number, em.e_mail
            FROM client c
            JOIN phone_numbers pn ON c.client_id = pn.client_id
            JOIN e_mails em ON c.client_id = em.client_id
            WHERE pn.phone_number = %s;
        """, (phone,))
        client_info = cur.fetchall()
        if len(client_info) != 0:
            print(f'\nClients id - {client_info[0][0]} \nClients first name - {client_info[0][1]} \n'
                  f'Clients last name - {client_info[0][2]} \n')
            client_id = client_info[0][0]
            cur.execute("""
                    SELECT client_id, phone_number
                        FROM phone_numbers
                        WHERE client_id = %s;
                    """, (client_id,))
            client_p_n = cur.fetchall()
            print(f'Client has phone numbers:')
            for i in client_p_n:
                print(i[1])
            cur.execute("""
                    SELECT client_id, e_mail
                        FROM e_mails
                        WHERE client_id = %s;
                    """, (client_id,))
            client_e_m = cur.fetchall()
            print(f'\nClient has e-mails:')
            for i in client_e_m:
                print(i[1])
        else:
            print(f'Can not identify any client.')
    else:
        print('Not enough data.')


database_name = input('Enter data base name: ')

user_name = input('Enter user name: ')

password_ = input('Enter password: ')


while True:

    help = '''\n\n1 - create data base
    2 - add client
    3 - add phone
    4 - change client 
    5 - delete phone
    6 - delete client
    7 - find client
    "-" - exit'''


    command = input(f'\nChoose command from the list: {help}\n')

    if command == '1':
        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                create_db(conn)
        conn.close()

    elif command == '2':
        print('Enter client first name \n\tTo go back to the main menu enter "-": ')
        while True:
            client_f_n = input()
            if client_f_n == '-':
                break
            if client_f_n is None or client_f_n.isspace() or not client_f_n.isalpha():
                print('\tClient should have first name. First name must be composed of letters.')
            else:
                break
        if client_f_n == '-':
            continue

        print('Enter client last name \n\tTo go back to the main menu enter "-": ')
        while True:
            client_l_n = input()
            if client_l_n == '-':
                break
            if client_l_n is None or client_l_n.isspace() or not client_l_n.isalpha():
                print('\tClient should have last name. Last name must be composed of letters.')
            else:
                break
        if client_l_n == '-':
            continue

        client_e_m = []
        print('Enter client e-mail(s) \n\tTo stop the entrance enter or to go back to the main menu enter "-": ')
        while True:
            e_m = input()
            if e_m == '-':
                if len(client_e_m) == 0:
                    print('\nClient should have at least one e-mail address. To go back to the main menu enter "-"')
                    d = input()
                    if d == '-':
                        break
                    else:
                        client_e_m.append(d)
                else:
                    break
            else:
                if e_m is None or e_m.isspace() or e_m == '':
                    print('\tTry again.')
                elif e_m in client_e_m:
                    print(f'\tYou have already entered "{e_m}".')
                else:
                    client_e_m.append(e_m)
                    if '-' in client_e_m:
                        client_e_m.remove('-')
        if len(client_e_m) == 0:
            continue

        client_p = []
        print('Enter client phone number(s) \n\tTo stop the entrance enter "-": ')
        while True:
            p_n = input()
            if p_n == "-":
                break
            if not p_n.isdigit() or len(p_n) != 10:
                print('\tPhone number should consists of ten digits.')
            elif int(p_n) in client_p:
                print(f'\tYou have already entered "{p_n}".')
            else:
                client_p.append(int(p_n))

        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                add_client(conn, first_name=client_f_n, last_name=client_l_n, client_e_mails=client_e_m, client_phones=client_p)
        conn.close()

    elif command == '3':
        print('Enter client id \n\tTo go back to the main menu enter "-": ')
        while True:
            id = input()
            if id == '-':
                break
            try:
                id = int(id)
                break
            except ValueError:
                print('\tId should be integer.')
        if id == '-':
            continue

        phone_numbers = []
        print('Enter client phone number(s) \n\tTo stop the entrance or to go back to the main menu enter "-" ')
        while True:
            p_n = input()
            if p_n == "-":
                break
            if len(p_n) != 10:
                print('\nPhone number must be ten digits.')
            elif int(p_n) in phone_numbers:
                print(f'\nYou have already entered "{p_n}".')
            else:
                try:
                    p_n = int(p_n)
                    phone_numbers.append(p_n)
                except ValueError:
                    print('\nWrong data format. Try again.')


        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                add_phone(conn, client_id=id, phones=phone_numbers)
        conn.close()

    elif command == '4':
        print('Enter client id \n\tTo go back to the main menu enter "-": ')
        while True:
            id = input()
            if id == '-':
                break
            try:
                id = int(id)
                break
            except ValueError:
                print('\tId should be integer.')
        if id == '-':
            continue

        print('Enter client first name \n\tTo keep current first name enter "-": ')
        while True:
            client_f_n = input()
            if client_f_n == '-':
                break
            if client_f_n is None or client_f_n == ' ' or not client_f_n.isalpha():
                print('\tFirst name should consists of letters.')
            else:
                break

        print('Enter client last name \n\tTo keep current last name enter "-": ')
        while True:
            client_l_n = input()
            if client_l_n == '-':
                break
            if client_l_n is None or client_l_n == ' ' or not client_l_n.isalpha():
                print('\tLast name should consists of letters.')
            else:
                break

        client_e_m = []
        print('Enter client e-mail(s) \n\tTo stop the entrance enter "-": ')
        while True:
            e_m = input()
            if e_m == "-":
                break
            if e_m is None or e_m.isspace() or e_m == '':
                print('\tTry again.')
            elif e_m in client_e_m:
                print(f'\tYou have already entered "{e_m}".')
            else:
                client_e_m.append(e_m)

        client_p = []
        print('Enter client phone number(s) \n\tTo stop the entrance enter "-": ')
        while True:
            p_n = input()
            if p_n == "-":
                break
            if not p_n.isdigit() or len(p_n) != 10:
                print('\tPhone number should consists of ten digits.')
            elif p_n in client_p:
                print(f'\tYou have already entered "{p_n}".')
            else:
                client_p.append(p_n)

        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                change_client(conn, client_id=id, first_name=client_f_n, last_name=client_l_n, emails=client_e_m, phones=client_p)
        conn.close()

    elif command == '5':
        print('Enter client id \n\tTo go back to the main menu enter "-": ')
        while True:
            id = input()
            if id == '-':
                break
            try:
                id = int(id)
                break
            except ValueError:
                print('Id should be integer.')
        if id == '-':
            continue

        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                delete_phone(client_id=id)
        conn.close()

    elif command == '6':
        print('Enter client id \n\tTo go back to the main menu enter "-": ')
        while True:
            id = input()
            if id == '-':
                break
            try:
                id = int(id)
                break
            except ValueError:
                print('Id should be integer.')
        if id == '-':
            continue

        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                delete_client(conn, client_id=id)
        conn.close()

    elif command == '7':

        print('Enter client first name \n\tTo cancel first name entrance enter "-": ')
        while True:
            client_f_n = input()
            if client_f_n == '-':
                client_f_n = None
                break
            if client_f_n is None or client_f_n == ' ' or not client_f_n.isalpha():
                print('\tFirst name should consists of letters.')
            else:
                break

        print('Enter client last name \n\tTo cancel last name entrance enter "-": : ')
        while True:
            client_l_n = input()
            if client_l_n == '-':
                client_l_n = None
                break
            if client_l_n is None or client_l_n == ' ' or not client_l_n.isalpha():
                print('\tLast name should consists of letters.')
            else:
                break

        print('Enter client e-mail \n\tTo cancel e-mail entrance enter "-": ')
        while True:
            e_m = input()
            if e_m == "-":
                e_m = None
                break
            if e_m is None or e_m.isspace() or e_m == '':
                print('\tTry again.')
            else:
                break


        print('Enter client phone number \n\tTo cancel phone number entrance enter "-": ')
        while True:
            p_n = input()
            if p_n == "-":
                p_n = None
                break
            if not p_n.isdigit() or len(p_n) != 10:
                print('\tPhone number should consists of ten digits.')
            else:
                break

        with psycopg2.connect(database=database_name, user=user_name, password=password_) as conn:
            with conn.cursor() as cur:
                find_client(conn, first_name=client_f_n, last_name=client_l_n, email=e_m, phone=p_n)
        conn.close()

    elif command == '-':
        print('\nGood bye!')
        break

    else:
        print(f'\nUnknown command.')