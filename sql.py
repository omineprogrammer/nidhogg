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
    query = "INSERT INTO %s(%s) VALUES(%s)" % (table,column,values)
    print query #[DEBUG]
    # return run_query(query)

def select(column, table, sentence = ''):
    query = "SELECT %s FROM %s %s" % (column,table,sentence)
    # print query #[DEBUG]
    return run_query(query)


def verifyv(value):
    if value == '':
        return 'NULL'
    elif type(value) is list:
        return value[0]
    else:
        return value


def insert_qinfo(data, code):
    """[["2017-01-10 12:30:15", 10,20,30],
        ["2017-01-10 12:30:15", 10,20,30]]"""

    table = 'QINFO'
    column = "Client_id, date, cpu, ram, hdd"
    id = (select("id", "client", "WHERE code = '" + code + "'"))[0][0]

    for i in data:
        values = ""
        values += "%d" % (id)
        values += ", '%s'" % (i[0])
        values += ", '%s'" % (verifyv(i[1]))
        values += ", '%s'" % (verifyv(i[2]))
        values += ", '%s'" % (verifyv(i[3]))

        insert(table, column, values)


def insert_info(data, code):
    """"""

    id = (select("id", "client", "WHERE code = '" + code + "'"))[0][0]

    for i in data:
        date = i[0]
        for property in i[1].keys():

            if property == "NICCONFIG":
                table = 'NICCONFIG'
                column = "Client_id, date, mac, ip, subnet, gateway, dns, name"
                for v in i[1][property]:
                    values = ""
                    values += "%d" % (id)
                    values += ", '%s'" % date
                    values += ", '%s'" % (v['MACAddress'])
                    values += ", '%s'" % (verifyv(v['IPAddress']))
                    values += ", '%s'" % (verifyv(v['IPSubnet']))
                    values += ", '%s'" % (verifyv(v['DefaultIPGateway']))
                    values += ", '%s'" % (verifyv(v['DNSServerSearchOrder']))
                    values += ", '%s'" % (v['Description'])
                    insert(table, column, values)

            elif property == "DISKDRIVE":
                table = 'DISKDRIVE'
                column = "Client_id, date, index, interfacetype, model, serialnumber, size"
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
                column = "Client_id, date, installdate, installsource, localpackage, name, vendor, version"
                for v in i[1][property]:
                    #validar registro
                    if (v['Name'] != '' and v['Vendor'] !=''):
                        values = ""
                        values += "%d" % (id)
                        values += ", '%s'" % date
                        values += ", '%s'" % (verifyv(v['InstallDate']))
                        values += ", '%s'" % (verifyv(v['InstallSource']))
                        values += ", '%s'" % (v['LocalPackage'])
                        values += ", '%s'" % (verifyv(v['Name']))
                        values += ", '%s'" % (verifyv(v['Vendor']))
                        values += ", '%s'" % (verifyv(v['Version']))
                        insert(table, column, values)

            else:
                for v in i[1][property]:
                    print v




