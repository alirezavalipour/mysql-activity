# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import mysql.connector
import time as tt
import os
from tabulate import tabulate
from argparse import ArgumentParser

from subprocess import call


# Press the green button in the gutter to run the script.

def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def clear():
    _ = call('clear' if os.name == 'posix' else 'cls')


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-H", "--host", dest="host", default="localhost", help="Host trying to connect", )
    parser.add_argument("-p", "--port", dest="port", default=3306, help="Port")
    parser.add_argument("-U", "--user", dest="user", help="user")
    parser.add_argument("-P", "--password", dest="password", help="password")
    parser.add_argument("-R", "--refreshrate", dest="refresh_rate", help="Refresh Rate")

    args = parser.parse_args()

    conn = mysql.connector.connect(
        port=args.port,
        host=args.host,
        user=args.user,
        passwd=args.password,
    )
    #
    # print(conn)
    # exit(1)
    cursor = conn.cursor(dictionary=True)

    headers = [

        # 'THREAD_ID',
        # 'NAME',
        # 'TYPE',
        'PROCESSLIST_ID',
        'PROCESSLIST_USER',
        'PROCESSLIST_HOST',
        'PROCESSLIST_DB',
        'PROCESSLIST_COMMAND',
        'PROCESSLIST_TIME',
        'PROCESSLIST_STATE',
        'PROCESSLIST_INFO',
        # 'PARENT_THREAD_ID',
        # 'ROLE',
        # 'INSTRUMENTED',
        # 'HISTORY',
        # 'CONNECTION_TYPE',
        # 'THREAD_OS_ID',
        # 'RESOURCE_GROUP',
        # 'EXECUTION_ENGINE',
        # 'CONTROLLED_MEMORY',
        # 'MAX_CONTROLLED_MEMORY',
        'TOTAL_MEMORY',
        # 'MAX_TOTAL_MEMORY',
    ]

    while True:
        try:
            cursor.execute("SELECT *  FROM performance_schema.threads")
        except mysql.connector.Error as err:
            print(err)

        table = []

        for row in cursor:
            newRow = []
            if row["PROCESSLIST_INFO"] == "SELECT *  FROM performance_schema.threads":
                continue
            for key in headers:
                newRow.append(row[key])
            if newRow[0] is None:
                continue

            table.append(newRow)
        # print(table)

        print(tabulate(table, headers=headers, tablefmt="simple_outline"))
        tt.sleep(float(args.refresh_rate))
        clear()

    # Disconnecting from the server
    conn.close()
