## Tools for Logging & DB
import psycopg2

## create a connection
conn = psycopg2.connect(
    host="localhost",
    database="lexbolo_db",
    user="lexbolo_pguser",
    password="--lexbolo+")

def get_benchmark():
    cur = conn.cursor()
    cur.execute('select * from benchmark order by time_needed')

    row = cur.fetchone()
    while row is not None:
        print(row)
        row = cur.fetchone()
    print("get_benchmark() done.")


def log_benchmark(model_name,prompt, time_needed, result):

    statement = "insert into benchmark(modelname, prompt, time_needed,result) VALUES (%s,%s,%s,%s)"
    # " + model_name + "','"+ prompt +"',"+ str(time_needed) +",quote_literal('"+ result +"'
    cur = conn.cursor()
    # print(statement)
    cur.execute(statement, (model_name,prompt,time_needed,result))
    conn.commit()
    cur.close()

#log_benchmark("test2","q2",9.368,"answer");




def show_pg_version():
    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
    cur.close()

#show_pg_version()
#get_benchmark()