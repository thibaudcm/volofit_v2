# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:40:51 2025

@author: thiba
"""

# optimizer.py

import math
from itertools import combinations
from plane import Plane

def assign_planes(data,
                  hub,
                  destination,
                  category,
                  eco_demand, 
                  bus_demand, 
                  fir_demand, 
                  car_demand, 
                  percent_in_addition,
                  tight_schedule=False,
                  demand_completion=False):
    
    Plane.remove_hub_to_dest(hub, destination)    
    
    eco_seats_demand  = math.ceil(eco_demand / 2)
    bus_seats_demand  = math.ceil(bus_demand / 2)
    fir_seats_demand  = math.ceil(fir_demand / 2)
    tot_seats_demand = math.ceil(eco_seats_demand + bus_seats_demand * 1.8 + fir_seats_demand * 4.2)
    car_route_demand  = math.ceil(car_demand / 2)

    data = data[data['category'] <= category]
    if tight_schedule:
        data = data[data['speed'] >= 903]

    target = tot_seats_demand *(1+(percent_in_addition/100))    
    best_score = float('inf')
    best_combo = None
    
    for r in range(1, 3):
        for combo in combinations(data.itertuples(index=False), r):
            tot_capacity = sum(plane.capacity for plane in combo)
            
            diff = target - tot_capacity
            if demand_completion:
                if diff <= 0 and abs(diff) < best_score:
                    best_score = abs(diff)
                    best_combo = combo
            else:
                if abs(diff) < best_score:
                    best_score = abs(diff)
                    best_combo = combo

    planes = [Plane(hub, destination, i, e.manufacturer, e.plane_name, e.capacity, e.price) for i, e in enumerate(best_combo) ]

    # Plane(s) filling
    if len(planes) == 1:
        p = planes[0]
        p.eco = eco_seats_demand
        p.bus = bus_seats_demand
        p.fir = fir_seats_demand
        p.car = car_route_demand
        if p.number_of_seats > p.capacity:
            excess = p.capacity - p.number_of_seats
            p.adjust_seats(excess)
    else:
        p1, p2 = planes
        capacity1 = p1.capacity
        eco_prop = eco_seats_demand         /   tot_seats_demand
        bus_prop = (bus_seats_demand * 1.8) /   tot_seats_demand
        fir_prop = (fir_seats_demand * 4.2) /   tot_seats_demand
    
        p1.eco = math.floor( capacity1 * eco_prop)
        p1.bus = math.floor((capacity1 * bus_prop) / 1.8)
        p1.fir = math.floor((capacity1 * fir_prop) / 4.2)
        p1.car = car_route_demand // 2 + car_route_demand % 2
    
        while p1.number_of_seats <= capacity1:
            p1.eco += 1
        p1.eco -= 1
    
        p2.eco = eco_seats_demand - p1.eco
        p2.bus = bus_seats_demand - p1.bus
        p2.fir = fir_seats_demand - p1.fir
        p2.car = car_route_demand // 2
    
        excess = (p1.capacity + p2.capacity) - tot_seats_demand
        p2.adjust_seats(excess)