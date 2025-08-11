import ctypes
import json
import os
import plotly.express as px
import streamlit as st
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def update_selected_cities():
    """Callback function to update session state with selected cities."""
    logging.info("Updating selected cities.")
    st.session_state["selected_cities"] = st.session_state["cities"]


def select_cities():
    """Select cities and return latitudes and longitudes."""
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

    # Initialize session state if not yet done
    if "selected_cities" not in st.session_state:
        st.session_state["selected_cities"] = []

    # Create the multiselect widget with callback
    logging.info("Creating multiselect widget for city selection.")
    st.multiselect(
        "Select cities for the shortest path problem:",
        options=[city["label"] for city in city_options],
        key="cities",  # This key is used in the callback
        on_change=update_selected_cities,  # Call the update function when selection changes
    )

    # When submit button is clicked
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

    return [], []  # In case no cities are selected yet


def build_shortest_path(latitudes, longitudes):
    """Build and display the shortest path on the map."""
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

    # Convert latitudes and longitudes to ctypes arrays
    num_cities = len(latitudes)
    lat_array = (ctypes.c_double * num_cities)(*latitudes)
    lon_array = (ctypes.c_double * num_cities)(*longitudes)

    cost = lib.build_path(num_cities, lat_array, lon_array)
    logging.info(f"Shortest path calculated with total cost: {cost} km.")

    # Create and display the plot using Plotly
    fig = px.line_geo(
        lat=[*lat_array], lon=[*lon_array], markers=True, projection="orthographic"
    )
    fig.update_geos(
        visible=False, resolution=50, showcountries=True, countrycolor="RebeccaPurple"
    )
    logging.info("Displaying path on map.")
    st.plotly_chart(fig)
