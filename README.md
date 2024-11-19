# Global Airport Route Optimizer

**Description**:
The **Global Airport Route Optimizer** is a Python-based web application that allows users to select airports across the world and calculates the shortest route to travel through all the selected airports solving the Traveling Salesman Problem (TSP) using Dynamic Programming algorithm. This project uses a combination of Python for the interface and C++ for efficient computation of the shortest path, ensuring fast and accurate results.

## Features and How It Works

- **Data Collection**: The app fetches airport data from the [AirportGap API](https://airportgap.com/api), which provides real-time airport information including latitude and longitude coordinates.

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

Make sure you have Python 3.x installed. You'll also need **C++** for the algorithm computation.

### Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/EldarKusdavletov/Global-Aviation-Route-Optimizer.git
   cd Global-Aviation-Route-Optimizer
   ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Compile the C++ code into a shared object (.so file):
    ```bash
    g++ -shared -o main.so -fPIC main.cpp
    ```

4. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```

## Contributions
Contributions are welcome! If you want to contribute to this project, please fork the repository, create a new branch, and submit a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/EldarKusdavletov/Global-Aviation-Route-Optimizer/blob/master/LICENSE) file for details.
