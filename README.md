# Global Airport Route Optimizer

**Description**:
The **Global Airport Route Optimizer** is a Python-based web application that allows users to select airports across the world and calculates the shortest route to travel through all the selected airports solving the Traveling Salesman Problem (TSP) using Dynamic Programming algorithm. This project uses a combination of Python for the interface and C++ for efficient computation of the shortest path, ensuring fast and accurate results.

## Features and How It Works

- **Data Collection**: The app fetches airport data from the [AirportGap API](https://airportgap.com/), which provides real-time airport information including latitude and longitude coordinates.

- **User Interface**: Built using **Streamlit**, the app allows users to select multiple airports from a global list using a user-friendly multiselect dropdown interface.

- **Optimization**: The shortest route algorithm is implemented in **C++** which is compiled into a shared object (.so) file and integrated into Python using **ctypes** to ensure high-performance computation.

- **Visualization**: The optimized route is displayed on an interactive map using **Plotly**, providing users with a visual representation of their travel route.

## Tech Stack

- **Python**: Main programming language for the app's logic and web interface.
- **Streamlit**: Framework for building the interactive web app.
- **Plotly**: Visualization library for rendering interactive maps.
- **C++**: Used for solving the TSP using dynamic programming.
- **ctypes**: Interface to integrate C++ functionality into Python.

## Installation

To run this project locally, follow these steps:

### Prerequisites

Make sure you have Python 3 installed.

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/EldarKusdavletov/Global-Aviation-Route-Optimizer.git
   cd Global-Aviation-Route-Optimizer
   ```
2. Create virtual environment and install the required Python packages
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. (OPTIONAL) Compile the C++ code into a shared object (.so file):
    ```bash
    g++ -O2 -shared -fPIC -o src/cpp/main.so src/cpp/tsp_solver.cpp
    ```

4. Run the Streamlit app:
- To launch the app normally:
    ```bash
    streamlit run src/python/main.py
    ```
- To refresh the airport data before launching the app, use the ```--refresh``` flag:
    ```bash
    streamlit run src/python/main.py -- --refresh
    ```
    This will download the latest airport data from the API and update the data/data.json file before the app starts.

## Contributions
Contributions are welcome! If you want to contribute to this project, please fork the repository, create a new branch, and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/EldarKusdavletov/Global-Aviation-Route-Optimizer?tab=MIT-1-ov-file) file for details.
