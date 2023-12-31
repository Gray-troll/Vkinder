import psycopg2


with psycopg2.connect(database="netology", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        conn.autocommit = True

def create_table_seen_person():
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS seen_person(
            id serial NOT NULL,
            id_vk varchar(50) PRIMARY KEY
            )"""
        )

def insert_data_seen_person(id_vk):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO seen_person (id_vk) 
           VALUES (%s)""",
            (id_vk,)
            )

                 

def check():
    check_data="SELECT * FROM seen_person"
    with conn.cursor() as cursor:
        cursor.execute(check_data)       
        return cursor.fetchall()
         

def delete_table_seen_person():
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS seen_person CASCADE;"""
        )


create_table_seen_person()
print("Database was created!")


