'''
DS 3500 Spring 2024
filename: clothes_objects.py
HW 3: dashboard
Kaydence Lin

Clothes Objects
'''

class Clothes:

    def __init__(self, brand, category, color, size, material, price, id = None):
        self.id = id
        self.brand = brand
        self.category = category
        self.color = color
        self.size = size
        self.material = material
        self.price = price