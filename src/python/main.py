import argparse
import logging
import streamlit as st
from app_ui import select_cities, build_shortest_path
from data_fetcher import refresh_airports_data

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main(refresh: bool):
    """Main function to run the Streamlit app."""
    logging.info("Starting Global Airport Route Optimizer app.")

    if refresh and "refresh" not in st.session_state:
        logging.info("Refresh flag set. Refreshing airport data.")
        refresh_airports_data("https://airportgap.com/api/airports", "../../data/data.json")
        st.write("Airport data refreshed successfully!")
        st.session_state["refresh"] = False

    latitudes, longitudes = select_cities()

    if latitudes and longitudes:
        logging.info(f"Proceeding to build shortest path for {len(latitudes)} cities.")
        build_shortest_path(latitudes, longitudes)
    else:
        logging.warning("No cities selected. Skipping path calculation.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Global Airport Route Optimizer")
    parser.add_argument(
        "--refresh", action="store_true", help="Refresh airport data from API"
    )
    args = parser.parse_args()

    logging.info("Application started.")
    main(args.refresh)
