import os

import psycopg2

def create_tables(conn):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40),
        last_name VARCHAR(40),
        email VARCHAR(50) CHECK (email LIKE '%_@__%.__%') UNIQUE 
    );
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS client_phone(
        id INTEGER REFERENCES clients(id),
        phone VARCHAR(15), CHECK(phone !~ '[:alpha:]'));
    ''')

def get_client_id(conn, email: str) -> int:
    cur.execute("""
    SELECT id FROM clients WHERE email=%s;
    """, (email,))
    return cur.fetchone()[0]

def add_client(conn, first_name, last_name, email, phone=None):
    cur.execute('''
    INSERT INTO clients(first_name, last_name, email)
    VALUES(%s, %s, %s);
    ''', (first_name, last_name, email))
    conn.commit()
    if phone != None:
        client_id = get_client_id(cur, email)
        cur.execute('''
        INSERT INTO client_phone(id, phone)
        VALUES(%s, %s);
        ''', (client_id, phone))

def add_phone(conn, client_id, phone):
    cur.execute('''
    INSERT INTO client_phone(id, phone)
    VALUES(%s, %s);
    ''', (client_id, phone))

# работа функции исправлена
def update_client_info(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
    UPDATE clients
    SET 
    first_name = COALESCE(%s, first_name),
    last_name = COALESCE(%s, last_name),
    email = COALESCE(%s, email)
    WHERE id=%s;
    UPDATE client_phone
    SET 
    phone = COALESCE(%s, phone)
    WHERE id=%s;
    ''', (first_name, last_name, email, client_id, phone, client_id))

def delete_phone(conn, client_id, phone):
    cur.execute('''
    DELETE FROM client_phone
    WHERE id=%s AND phone=%s
    ''', (client_id, phone))
    conn.commit()

def delete_client(conn, client_id):
    cur.execute('''
    DELETE FROM client_phone
    WHERE id=%s;
    DELETE FROM clients
    WHERE id=%s;
    ''', (client_id, client_id))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
    SELECT clients.id FROM clients
    LEFT JOIN client_phone ON clients.id = client_phone.id 
    WHERE phone=%s
    OR first_name=%s
    OR last_name=%s
    OR email=%s;
    ''', (phone, first_name, last_name, email))
    print(cur.fetchone()[0])

if __name__ == '__main__':

    database = os.getenv('database')
    user = os.getenv('user')
    password = os.getenv('password')

    with psycopg2.connect(database=database, user=user, password=password) as conn:
        with conn.cursor() as cur:

            # create_tables(conn)
            # add_client(conn, 'mick', 'Jagger', 'Mick@rs.uk')
            add_phone(conn, 1, '79216380318')
            # update_client_info(conn, 1, first_name='John', email='kika@yandex.ru')
            # delete_phone(conn, 1, '99999')
            # delete_client(conn, 1)
            # find_client(conn, email='Mick@rs.uk')