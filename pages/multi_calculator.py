# streamlit_page: Multi calculator 🚀

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
    streamlit run multi_calculator.py
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

# =============================================================================
#  Inputs
# =============================================================================

with st.form("input_form"):
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
    submitted = st.form_submit_button("✈️ Calculate and save")

# =============================================================================
# Data Tables
# =============================================================================

if "planes" not in st.session_state:
    st.session_state.planes = []

if submitted:
    data = pd.read_csv('planes.csv', sep=';')
    assign_planes(data, hub, dest, category, eco_demand, bus_demand, fir_demand, car_demand, 0, tight_schedule, demand_completion)

if Plane.get_by_manufacturer('Airbus'):
    st.subheader("📊 Airbus aircraft to buy")
    airbus_planes = Plane.get_by_manufacturer('Airbus')
    df_airbus = pd.DataFrame([plane.to_dict() for plane in airbus_planes])
    st.dataframe(df_airbus, use_container_width=True)
    total_price_airbus = sum(plane.price for plane in airbus_planes)
    st.markdown(f"**Total price for Airbus planes:** ${total_price_airbus:,}")

if Plane.get_by_manufacturer('Boeing'):
    st.subheader("📊 Boeing aircraft to buy")
    boeing_planes = Plane.get_by_manufacturer('Boeing')
    df_boeing = pd.DataFrame([plane.to_dict() for plane in boeing_planes])
    st.dataframe(df_boeing, use_container_width=True)
    total_price_boeing = sum(plane.price for plane in boeing_planes)
    st.markdown(f"**Total price for Boeing planes:** ${total_price_boeing:,}")
    
    if "total_price_airbus" not in globals():
        total_price_airbus = 0
    if "total_price_boeing" not in globals():
        total_price_boeing = 0
    st.metric("Total price", f"{total_price_airbus+total_price_boeing:,} $")
    
if Plane.get_hub_to_dest(hub, dest):
    planes = Plane.get_hub_to_dest(hub, dest)
    st.subheader("📊 Résumé global")

    col1, col2, col3 = st.columns(3)

    tot_capacity = sum(plane.capacity for plane in planes)
    occupied_seats = sum(plane.number_of_seats for plane in planes) 
    col1.metric("Total capacity", tot_capacity)
    col2.metric("Occupied seats", f"{occupied_seats:.1f}")
    col3.metric("Empty seats", f"{tot_capacity - occupied_seats:.1f}")

    tot_seats_demand = (eco_demand/2) + (bus_demand/2)*1.8 + (fir_demand/2)*4.2
    col1.metric("Seats demand", tot_seats_demand)
    demand_covered = 100 * occupied_seats / tot_seats_demand  
    col2.metric("Demand covered", f"{demand_covered:.1f} %")
    car_demand_covered = 100 * (sum(p.car for p in planes))/ (car_demand/2)
    col3.metric("Cargo demand covered", f"{car_demand_covered:.1f} %")
    
# =============================================================================
# Deleting existing lines
# =============================================================================

existing_lines = list({f"{p.hub}-{p.destination}" for p in Plane.get_all()})

if existing_lines:
    st.subheader("🗑️ Delete an existing line")
    line_to_delete = st.selectbox("Select the line you want to delete", existing_lines)

    if st.button("Delete this line"):
        Plane.remove_line(line_to_delete)
        st.session_state["delete_message"] = f"Line {line_to_delete} removed"  # Stocké immédiatement
        st.rerun() 
        
if "delete_message" in st.session_state:
    st.success(st.session_state["delete_message"])
    del st.session_state["delete_message"]
    
# =============================================================================
# Downloading data
# =============================================================================
    
dfs = []

if "df_airbus" in locals() and not df_airbus.empty:
    df_airbus["Type"] = "Airbus"
    dfs.append(df_airbus)

if "df_boeing" in locals() and not df_boeing.empty:
    df_boeing["Type"] = "Boeing"
    dfs.append(df_boeing)
    
if dfs:
    df_all = pd.concat(dfs, ignore_index=True)
    csv = df_all.to_csv(index=False, sep=';')
    st.download_button(
        label="📥 Download data (CSV)",
        data=csv,
        file_name="aircraft_lines_data.csv",
        mime="text/csv"
    )
