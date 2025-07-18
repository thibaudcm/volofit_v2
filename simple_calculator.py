# streamlit_page: Simple calculator 🚀

# -*- coding: utf-8 -*-
"""
=============================================================================
VoloFit – Smart Aircraft Allocator for Airlines Manager
=============================================================================

main.py – Optimizer for aircraft combinations to maximize passenger and cargo load

Author   : thibaudcm  
Date     : 2025-07-16
Version  : 2.0
Description :  
This script suggests the best combination of aircraft to meet passenger and cargo demand  
in the game Airlines Manager. It provides an optimal allocation based on current needs.  

Usage:  
    streamlit run simple_calculator.py
"""

# =============================================================================
# Importing lib
# =============================================================================

import streamlit as st
import pandas as pd
from plane import Plane
from optimizer import assign_planes 

# =============================================================================
# Page setup
# =============================================================================

st.set_page_config(
    page_title="VoloFit",
    layout ="centered",
    page_icon="✈️",
    initial_sidebar_state="collapsed"
)
st.title("✈️ VoloFit - Smart Aircraft Allocator for Airlines Manager")
Plane.clear()

# =============================================================================
#  Inputs
# =============================================================================

col1, col2, col3 = st.columns(3)
with col1:
    hub = st.text_input("Departure Hub", value="CDG")
with col2:
    dest = st.text_input("Destination", value="HND")
with col3:
    category = st.number_input("Category", min_value=1, max_value=10, value=10)
eco_demand = st.number_input("🧍 Economy Class demand", min_value=0, value=1000)
bus_demand = st.number_input("🧑‍💼 Business Class demand", min_value=0, value=200)
fir_demand = st.number_input("🧑‍✈️ First Class demand", min_value=0, value=100)
car_demand = st.number_input("📦 Cargo demand", min_value=0, value=10)

col1, col2 = st.columns(2)
with col1:
    tight_schedule = st.checkbox("Tight schedule : flight time >= 23h30", value=False)
with col2:
    demand_completion = st.checkbox("Cover full demand", value=True)

# =============================================================================
# Data Tables
# =============================================================================

if "planes" not in st.session_state:
    st.session_state.planes = []

data = pd.read_csv('planes.csv', sep=';')
assign_planes(data, hub, dest, category, eco_demand, bus_demand, fir_demand, car_demand, 0, tight_schedule, demand_completion)

if Plane.get_all():
    st.subheader("📊 Aircraft")
    df = pd.DataFrame([plane.to_dict() for plane in Plane.get_all()])
    st.dataframe(df, use_container_width=True)
    total_price = sum(plane.price for plane in Plane.get_all())
    st.markdown(f"**Total price :** ${total_price:,}")   

st.subheader("📊 Résumé global")

col1, col2, col3 = st.columns(3)

tot_capacity = sum(plane.capacity for plane in Plane.get_all())
occupied_seats = sum(plane.number_of_seats for plane in Plane.get_all()) 
col1.metric("Total capacity", tot_capacity)
col2.metric("Occupied seats", f"{occupied_seats:.1f}")
col3.metric("Empty seats", f"{tot_capacity - occupied_seats:.1f}")

tot_seats_demand = (eco_demand/2) + (bus_demand/2)*1.8 + (fir_demand/2)*4.2
col1.metric("Seats demand", tot_seats_demand)
demand_covered = 100 * occupied_seats / tot_seats_demand  
col2.metric("Demand covered", f"{demand_covered:.1f} %")
car_demand_covered = 100 * (sum(p.car for p in Plane.get_all()))/ (car_demand/2)
col3.metric("Cargo demand covered", f"{car_demand_covered:.1f} %")