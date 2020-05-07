import os
import time
import psycopg2
from psycopg2 import pool
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from multiprocessing import Process

class Pgpool:
    def __init__(self):
        self.postgresPool = psycopg2.pool.SimpleConnectionPool(1,20,
                                                          user="media",
                                                          password="123123",
                                                          host="127.0.0.1",
                                                          port="5432",
                                                          database="media")
        print("success, create connection pool")
    def insert(self,datas):
        pgConnection = self.postgresPool.getconn()
        if(pgConnection):
            print("success, recived conntion from pool")
            pgCursor = pgConnection.cursor()
            print(datas)
            pgCursor.execute("INSERT INTO test_data (datas) VALUES (%s);",(datas,))
            # result = pgCursor.fetchall()
            # for row in result:
            #     print(row)
            pgConnection.commit()
            pgConnection.close()

class Observing:

    def __init__(self,path,handler):
        self.observer = Observer()   #observer객체를 만듦
        self.observer.schedule(handler, path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()
            self.observer.start()

class Otm1Handler(FileSystemEventHandler):

    def on_deleted(self, event): #파일, 디렉터리가 생성되면 실행
        checktime()
        # print(event.src_path)
        # file = open(event.src_path, 'r')
        # content = file.readline()
        # print(type(content))
        # pgpool.insert(content)

class Otm2Handler(FileSystemEventHandler):

    def on_created(self, event):
        checktime()

def checktime():
    start = time.time()
    print("otm1 starttime:", start)
    for i in range(20000000):
        i += i
    print("otm1 endtime", time.time())

if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
    pathPrefix="C:/Users/Byun/PycharmProjects/watchdogex/"

    observedPath=["otm/otm1","otm/otm2"]

    handlerList=[Otm1Handler(),Otm2Handler()]
    pathList=[pathPrefix+sub for sub in observedPath]

    print(pathList)
    pgpool = Pgpool() #스크립트 실행시 connection pool 생성


    for path, handler in zip(pathList, handlerList):
        p = Process(target=Observing, args=(path,handler))
        p.start()