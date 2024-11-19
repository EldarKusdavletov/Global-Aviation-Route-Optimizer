import ctypes
import json
import os
import plotly.express as px
import streamlit as st


def update_selected_cities():
    """Callback function to update session state with selected cities."""
    st.session_state["selected_cities"] = st.session_state["cities"]


def select_cities():
    with open("data/data.json") as f:
        data = json.load(f)

    # Prepare city options with city details
    city_options = [
        {
            "label": f"{airport['attributes']['city']} ({airport['attributes']['country']}) [{airport['id']}]",
            "latitude": float(airport["attributes"]["latitude"]),
            "longitude": float(airport["attributes"]["longitude"]),
        } for airport in data
    ]

    # Initialize session state if not yet done
    if "selected_cities" not in st.session_state:
        st.session_state["selected_cities"] = []

    # Create the multiselect widget with callback
    st.multiselect(
        "Select cities for the shortest path problem:",
        options=[city["label"] for city in city_options],
        key="cities",  # This key is used in the callback
        on_change=update_selected_cities  # Call the update function when selection changes
    )

    # When submit button is clicked
    if st.button("Submit"):
        # Extract latitudes and longitudes for selected cities
        latitudes = [city["latitude"] for city in city_options if city["label"] in st.session_state["selected_cities"]]
        longitudes = [city["longitude"] for city in city_options if city["label"] in st.session_state["selected_cities"]]
        return latitudes, longitudes

    return [], []  # In case no cities are selected yet


def build_shortest_path(latitudes, longitudes):
    if os.name == "nt":
        raise NotImplementedError("Not implemented for Windows")
    else:
        lib = ctypes.CDLL("./main.so")

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

    # Create and display the plot using Plotly
    fig = px.line_geo(
        lat=[*lat_array],
        lon=[*lon_array],
        markers=True,
        projection="orthographic"
    )
    fig.update_geos(
        visible=False,
        resolution=50,
        showcountries=True,
        countrycolor="RebeccaPurple"
    )
    st.plotly_chart(fig)


if __name__ == "__main__":
    latitudes, longitudes = select_cities()
    if latitudes and longitudes:  # Only build the path if cities are selected
        build_shortest_path(latitudes, longitudes)
