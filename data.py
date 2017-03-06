# -*- coding: utf-8 -*-

import sql
import json
import time


def decode(message):
    message = json.loads(message)
    return message


# def jsontree(self, message, indent = 2):
#     message = json.dumps(message, sort_keys = True, indent = indent)
#     return message

def verify(value):
    if value == '':
        return 'NULL'
    elif type(value) is list:
        return value[0]
    else:
        return value

# table = 'QINFO'
# column = "Client_id, date, cpu, ram, hdd"
# id = (sql.selectdb("id", "client", "WHERE code = '" + code + "'"))[0][0]
#
# for i in data[table]:
#     value = ""
#     value += "%d" % (id)
#     value += ", '%s'" % (i['MACAddress'])
#     value += ", '%s'" % (verify(i['IPAddress']))
#     value += ", '%s'" % (verify(i['IPSubnet']))
#     value += ", '%s'" % (verify(i['DefaultIPGateway']))
#     value += ", '%s'" % (verify(i['DNSServerSearchOrder']))
#     value += ", '%s'" % (i['Description'])
#
#     sql.insertdb(table, column, value)

if "NICCONFIG" in data.keys():
    table = 'NICCONFIG'
    column = "Client_id, mac, ip, subnet, gateway, dns, name"
    id = (sql.selectdb("id", "client", "WHERE code = '" + code + "'"))[0][0]

    for i in data[table]:
        value = ""
        value += "%d" % (id)
        value += ", '%s'" % (i['MACAddress'])
        value += ", '%s'" % (verify(i['IPAddress']))
        value += ", '%s'" % (verify(i['IPSubnet']))
        value += ", '%s'" % (verify(i['DefaultIPGateway']))
        value += ", '%s'" % (verify(i['DNSServerSearchOrder']))
        value += ", '%s'" % (i['Description'])

        sql.insertdb(table, column, value)
