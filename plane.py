# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 14:01:29 2025

@author: thiba
"""

class Plane:
    
    __list = []
    
    def __init__(self, hub, destination, ID, manufacturer, name, capacity, price):
        self.hub            = hub
        self.destination    = destination
        self.ID             = ID
        self.manufacturer   = manufacturer
        self.name           = name
        self.capacity       = capacity
        self.price          = price
        self.eco            = 0
        self.bus            = 0
        self.fir            = 0
        self.car            = 0
        Plane.__list.append(self)
        
    def to_dict(self):
        return {
            "Line": self.hub + "-" + self.destination + "-" + str(self.ID),
            #"Manufacturer": self.manufacturer,
            "Plane": self.name,
            "Capacity": self.capacity,
            #"Price": self.price,
            "Eco": self.eco,
            "Bus": self.bus,
            "Fir": self.fir,
            "Car": self.car
        }

    @property
    def number_of_seats(self):
        return self.eco + self.bus * 1.8 + self.fir * 4.2

    def adjust_seats(self, diff):
        a, b, c = 0, 0, 0
        while diff < 0:
            if self.fir - c > 0 and abs(diff) >= 4.2:
                c += 1
                diff += 4.2
            elif self.bus - b > 0 and abs(diff) >= 1.8:
                b += 1
                diff += 1.8
            elif self.eco - a > 0:
                a += 1
                diff += 1
            else:
                break
        self.eco -= a
        self.bus -= b
        self.fir -= c

    def infos(self):
        print(f"{self.hub:<3} {self.destination:<4} {self.ID:<1} {self.manufacturer:<6} {self.name:<10} {self.price:<10}$ {self.capacity:>4} {self.eco:>4} {self.bus:>4} {self.fir:>4} {self.car:>4}")
    
    @staticmethod
    def clear():
        Plane.__list = []
    @staticmethod 
    def get_all():
        return Plane.__list
    @staticmethod 
    def get_hub_to_dest(hub, dest):
        list = []
        for e in Plane.get_all():
            if e.hub == hub and e.destination == dest:
                list.append(e)
        return list
    @classmethod
    def remove_hub_to_dest(cls, hub, dest):
        cls.__list = [p for p in cls.__list if not (p.hub == hub and p.destination == dest)]
    @staticmethod 
    def all_infos():
        for e in Plane.get_all():
            e.infos()
    @staticmethod
    def get_by_manufacturer(name: str):
        return [plane for plane in Plane.get_all() if plane.manufacturer.lower() == name.lower()]
    @staticmethod
    def remove_line(line_code):
        hub, dest = line_code.split("-")
        Plane.__list = [p for p in Plane.get_all() if not (p.hub == hub and p.destination == dest)]