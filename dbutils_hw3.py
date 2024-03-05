"""
DS 3500 Spring 2024
filename: dbutils_hw3.py
HW 3: dashboard
Kaydence Lin and Tanishi Datta

Requires the driver:  conda install mysql-connector-python

description: A collection of database utilities to make it easier
to implement a database application
"""

import mysql.connector
import pandas as pd

class DBUtils:

    def __init__(self, user=None, password=None, database=None, host="localhost"):
        """ Initialize the DBUtils object """
        if user is None:
            user = input("Enter your MySQL username: ")
        if password is None:
            password = input("Enter your MySQL password: ")
        if database is None:
            database = input("Enter the name of the MySQL database: ")

        self.con = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def close(self):
        """ Close or release a connection back to the connection pool """
        self.con.close()
        self.con = None

    def execute(self, query, values=None):
        """ Execute a select query and returns the result as a dataframe """
        rs = self.con.cursor()

        if values:
            if isinstance(values, (list, tuple)):
                if isinstance(values, tuple):
                    rs.execute(query, values)
                else:
                    values = tuple(map(self.convert_mysql, values))
                    rs.execute(query, values)
            else:
                rs.execute(query, values)
        else:
            rs.execute(query)

        rows = rs.fetchall()
        cols = list(rs.column_names)

        rs.close()

        return pd.DataFrame(rows, columns=cols)

    def insert_one(self, sql, val):
        """ Insert a single row """
        cursor = self.con.cursor()
        cursor.execute(sql, val)
        self.con.commit()

    def insert_many(self, sql, vals):
        """ Insert multiple rows """
        cursor = self.con.cursor()
        cursor.executemany(sql, vals)
        self.con.commit()

    def convert_mysql(self, value):
        """Converts python types to MySQL types"""
        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()
        else:
            return value