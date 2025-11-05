import ctypes
import json
import os
import time
import plotly.graph_objects as go
import streamlit as st
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_selected_cities():
    logging.info("Updating selected cities.")
    st.session_state["selected_cities"] = st.session_state["cities"]


def select_cities():
    logging.info("Loading city data from 'data/data.json'.")
    with open("data/data.json") as f:
        data = json.load(f)
    logging.info(f"Loaded {len(data)} airports from data.")

    city_options = [
        {
            "label": f"{airport['attributes']['city']} ({airport['attributes']['country']}) [{airport['id']}]",
            "latitude": float(airport["attributes"]["latitude"]),
            "longitude": float(airport["attributes"]["longitude"]),
        }
        for airport in data
    ]

    if "selected_cities" not in st.session_state:
        st.session_state["selected_cities"] = []

    st.multiselect(
        "Select cities for the shortest path problem:",
        options=[city["label"] for city in city_options],
        key="cities",
        on_change=update_selected_cities,
    )

    if st.button("Submit"):
        latitudes = [
            city["latitude"]
            for city in city_options
            if city["label"] in st.session_state["selected_cities"]
        ]
        longitudes = [
            city["longitude"]
            for city in city_options
            if city["label"] in st.session_state["selected_cities"]
        ]
        logging.info(f"Selected {len(latitudes)} cities.")
        return latitudes, longitudes

    return [], []


def build_shortest_path(latitudes, longitudes):
    logging.info("Building shortest path.")
    if os.name == "nt":
        logging.error("Windows OS detected, feature not implemented for Windows.")
        raise NotImplementedError("Not implemented for Windows")
    else:
        lib = ctypes.CDLL("src/cpp/main.so")
        logging.info("Loaded C++ shared library.")

    lib.build_path.restype = ctypes.c_double
    lib.build_path.argtypes = [
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double),
        ctypes.POINTER(ctypes.c_double),
    ]

    num_cities = len(latitudes)
    lat_array = (ctypes.c_double * num_cities)(*latitudes)
    lon_array = (ctypes.c_double * num_cities)(*longitudes)

    cost = lib.build_path(num_cities, lat_array, lon_array)
    logging.info(f"Shortest path calculated with total cost: {cost} km.")

    start_plotting = time.time()

    fig = go.Figure(go.Scattermapbox(
        lat=[*lat_array],
        lon=[*lon_array],
        mode="markers+lines",
        marker=dict(size=7, color="red"),
    ))

    fig.update_layout(
        mapbox_style="open-street-map",  # No token required, still WebGL
        mapbox=dict(
            center=dict(lat=latitudes[0], lon=longitudes[0]),
            zoom=1,
        ),
        width=900,
        height=600,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    render_time = round((time.time() - start_plotting) * 1000, 2)
    logging.info(f"WebGL render time: {render_time} ms")
    logging.info("Displaying path on map.")
    st.plotly_chart(fig, use_container_width=True)
