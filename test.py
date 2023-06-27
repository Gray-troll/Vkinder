import psycopg2


with psycopg2.connect(database="netology", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        cur.execute ("CREATE TABLE test(id SERIAL PRIMARY KEY)")
        