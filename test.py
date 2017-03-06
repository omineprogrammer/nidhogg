# -*- coding: utf-8 -*-

import MySQLdb


def run_query(query = ''):
    db_host = 'localhost'
    db_user = 'root'
    db_pass = 'alfaromero'
    db_name = 'nidhogg'
    dbconnct = [db_host, db_user, db_pass, db_name]

    conn = MySQLdb.connect(*dbconnct)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
    except Exception as err:
        print err

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None

    cursor.close()
    conn.close()

    return data

def insertdb(table, column, values):
    query = "INSERT INTO %s (%s) VALUES %s" % (table,column,values)
    print query
    print run_query(query)

def selectdb(column, table, sentence = ''):
    query = "SELECT %s FROM %s %s" % (column,table,sentence)
    print query
    print run_query(query)

insertdb("client", "code, name", u"('GSVN2B', 'VILLA NUEVA 2')")
selectdb("*", "client", "WHERE name = 'VILLA NUEVA 2'")









# import subprocess
# import sys
#
#
# def cmd(cmmd):
#     temp = subprocess.Popen(cmmd, stdout = subprocess.PIPE, shell = True)
#     out = str(temp.stdout.read())
#     out = out.replace("\r", "")
#     out = out.replace("\n", "")
#     out = out.replace("\t", "")
#     return out
#
# out = cmd('vol')
# out = out[-9:]
# out.replace('-','')
#
# print out

#
#
# subprocess.call("wmic volume list brief", stdout = subprocess.PIPE)

#
#
#
# import threading
# import time
# def worker():
#     print threading.currentThread().getName(), 'Lanzado'
#     th = threading.currentThread()
#     print "th:", th
#     time.sleep(2)
#     print threading.currentThread().getName(), 'Deteniendo'
# def servicio():
#     print threading.currentThread().getName(), 'Lanzado'
#     print threading.currentThread().getName(), 'Deteniendo'
# t = threading.Thread(target=servicio, name='Servicio')
# w = threading.Thread(target=worker, name='Worker')
# z = threading.Thread(target=worker)
# w.start()
# z.start()
# t.start()



# import threading, time
#
#
# class MiThread(threading.Thread):
#     def __init__(self, evento):
#         threading.Thread.__init__(self)
#         self.evento = evento
#
#     def run(self):
#         print self.getName(), "esperando al evento"
#         self.evento.wait()
#         print self.getName(), "termina la espera"
#
#
# evento = threading.Event()
# t1 = MiThread(evento)
# t1.start()
# t2 = MiThread(evento)
# t2.start()
#
# # Esperamos un poco
# time.sleep(5)
# evento.set()