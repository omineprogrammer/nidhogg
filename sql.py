# -*- coding: utf-8 -*-

import MySQLdb
import logging

def mklogger(name):
    logging.basicConfig(filename = 'sql.log', level = logging.DEBUG,
        format = '%(asctime)s - %(name)-13s: %(levelname)-8s - %(message)s')
    logger = logging.getLogger(name)
    return logger


def run_query(query = ''):
    logger = mklogger("run_query")

    db_host = 'localhost'
    db_user = 'root'
    db_pass = 'alfaromero'
    db_name = 'nidhogg'
    dbconnct = [db_host, db_user, db_pass, db_name]

    conn = MySQLdb.connect(*dbconnct)
    cursor = conn.cursor()

    try:
        logger.debug("query: " + query)
        logger.debug("tipo dato quey: " + str(type(query)))
        cursor.execute(query)
    except Exception as err:
        logger.warning(err)
        conn.rollback()
        cursor.close()
        conn.close()

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None

    cursor.close()
    conn.close()

    return data


def insert(table, column, values):
    logger = mklogger("run_query")

    query = "INSERT INTO %s(%s) VALUES(%s)" % (table,column,values)
    logger.debug("query: " + query)
    print query #[DEBUG]
    # return run_query(query)

def select(column, table, sentence = ''):
    query = "SELECT %s FROM %s %s" % (column,table,sentence)
    # print query #[DEBUG]
    return run_query(query)

def verifys(value):
    if value == '':
        return 'NULL'
    elif type(value) is list:
        return value[0]
    else:
        return value

def verifyn(value):
    if value == '':
        return 0
    elif type(value) is list:
        return float(value[0])
    else:
        return float(value)



def insert_qinfo(data, code):
    """[["2017-01-10 12:30:15", 10,20,30],
        ["2017-01-10 12:30:15", 10,20,30]]"""

    table = 'QINFO'
    column = "id, date, cpu, ram, hdd"
    id = (select("id", "client", "WHERE code = '" + code + "'"))[0][0]
    # id = select(column = "id", table = "client", sentence = "WHERE code = '" + code + "'")[0][0]


    for i in data:
        values = ""
        values += "%d" % (id)
        values += ", '%s'" % (i[0])
        values += ", %.1f" % (verifyn(i[1]))
        values += ", %.1f" % (verifyn(i[2]))
        values += ", %.1f" % (verifyn(i[3]))

        insert(table, column, values)


def insert_info(data, code):
    """"""

    id = (select("id", "client", "WHERE code = '" + code + "'"))[0][0]

    for i in data:
        date = i[0]
        for property in i[1].keys():

            if property == "NICCONFIG":
                table = 'NICCONFIG'
                column = "id, date, mac, ip, subnet, gateway, dns, name"
                for v in i[1][property]:
                    values = ""
                    values += "%d" % (id)
                    values += ", '%s'" % date
                    values += ", '%s'" % (v['MACAddress'])
                    values += ", '%s'" % (verifys(v['IPAddress']))
                    values += ", '%s'" % (verifys(v['IPSubnet']))
                    values += ", '%s'" % (verifys(v['DefaultIPGateway']))
                    values += ", '%s'" % (verifys(v['DNSServerSearchOrder']))
                    values += ", '%s'" % (v['Description'])
                    insert(table, column, values)

            elif property == "DISKDRIVE":
                table = 'DISKDRIVE'
                column = "id, date, index, interfacetype, model, serialnumber, size"
                for v in i[1][property]:
                    values = ""
                    values += "%d" % (id)
                    values += ", '%s'" % date
                    values += ", '%s'" % (v['Index'])
                    values += ", '%s'" % (v['InterfaceType'])
                    values += ", '%s'" % (v['Model'])
                    values += ", '%s'" % (v['SerialNumber'])
                    values += ", '%s'" % (v['Size'])
                    insert(table, column, values)

            elif property == "PRODUCT":
                table = 'PRODUCT'
                column = "id, date, installdate, installsource, localpackage, name, vendor, version"
                for v in i[1][property]:
                    #validar registro
                    if (v['Name'] != '' and v['Vendor'] !=''):
                        values = ""
                        values += "%d" % (id)
                        values += ", '%s'" % date
                        values += ", '%s'" % (verifys(v['InstallDate']))
                        values += ", '%s'" % (verifys(v['InstallSource']))
                        values += ", '%s'" % (v['LocalPackage'])
                        values += ", '%s'" % (verifys(v['Name']))
                        values += ", '%s'" % (verifys(v['Vendor']))
                        values += ", '%s'" % (verifys(v['Version']))
                        insert(table, column, values)

            else:
                for v in i[1][property]:
                    print v
