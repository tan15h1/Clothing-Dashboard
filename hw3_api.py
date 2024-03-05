'''
DS3500 Spring 24
Tanishi Datta and Kaydence Lin
filename: hw3_api.py
HW3: Dashboards
Description: API for accessing data from sql
'''
from dbutils_hw3 import DBUtils

class ClothesAPI:

    def __init__(self, user = None, password = None, database = None, host = "localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def get_clothes(self, clothes):
        ''' Method to get all clothes and insert into database'''
        sql = "INSERT INTO clothing(id, brand, category, color, size, material, price) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (clothes.id, clothes.brand, clothes.category, clothes.color, clothes.size, clothes.material, clothes.price)
        self.dbu.insert_one(sql, val)

    def clothes_data(self, material=None, category=None):
        '''Method to get all brands, materials, prices, sizes, and categories from the clothing table'''
        query = "SELECT brand, material, size, price, category FROM Clothing WHERE 1=1"

        if material and material != 'All':
            query += f" AND material = '{material}'"
        if category and category != 'All':
            query += f" AND category = '{category}'"

        df = self.dbu.execute(query)
        return df