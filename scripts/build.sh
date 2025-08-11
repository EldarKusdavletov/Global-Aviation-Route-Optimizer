#!/bin/bash
set -e
g++ -O2 -shared -fPIC -o src/cpp/main.so src/cpp/tsp_solver.cpp