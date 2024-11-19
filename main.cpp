#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits>
#include <optional>
#include <vector>

std::vector<std::vector<double>> calculate_distance_matrix(const size_t size, const double *latitudes, const double *longitudes) {
    std::vector<std::vector<double>> distance_matrix(size, std::vector<double>(size, 0.0));

    auto haversine = [](double lat1, double lon1, double lat2, double lon2) {
        const double R = 6371.0;  // Earth's radius in kilometers
        double dlat = (lat2 - lat1) * M_PI / 180.0;
        double dlon = (lon2 - lon1) * M_PI / 180.0;
        lat1 = lat1 * M_PI / 180.0;
        lat2 = lat2 * M_PI / 180.0;
        double a = sin(dlat / 2) * sin(dlat / 2) + cos(lat1) * cos(lat2) * sin(dlon / 2) * sin(dlon / 2);
        double c = 2 * atan2(sqrt(a), sqrt(1 - a));
        return R * c;
    };

    for (size_t i = 0; i < size; ++i) {
        for (size_t j = i + 1; j < size; ++j) {
            distance_matrix[i][j] = distance_matrix[j][i] = haversine(latitudes[i], longitudes[i], latitudes[j], longitudes[j]);
        }
    }

    return distance_matrix;
}

double solve_tsp(const size_t size, const std::vector<std::vector<double>> &distance_matrix, size_t *path) {
    uint64_t num_states = 1 << size;
    std::vector<std::vector<std::optional<double>>> dp(size, std::vector<std::optional<double>>(num_states));

    for (size_t i = 0; i < size; ++i)
        dp[i][1 << i] = distance_matrix[i][i];

    for (size_t mask = 1; mask < num_states; ++mask) {
        for (size_t last = 0; last < size; ++last) {
            if (mask >> last & 1) {
                for (size_t next = 0; next < size; ++next) {
                    if (!(mask >> next & 1)) {
                        size_t new_mask = mask | 1 << next;
                        if (!dp[next][new_mask] || *dp[next][new_mask] > *dp[last][mask] + distance_matrix[last][next])
                            dp[next][new_mask] = *dp[last][mask] + distance_matrix[last][next];
                    }
                }
            }
        }
    }

    std::optional<double> cost;
    for (size_t last = 0; last < size; ++last) {
        if (!cost || *dp[last][num_states - 1] < *cost) {
            cost = *dp[last][num_states - 1];
            path[0] = last;
        }
    }

    size_t state = (num_states - 1) ^ 1 << path[0];
    for (size_t i = 1; i < size; ++i) {
        std::optional<size_t> index;
        for (size_t j = 0; j < size; ++j) {
            if (state >> j & 1) {
                if (!index || *dp[j][state] + distance_matrix[j][path[i - 1]] < *dp[*index][state] + distance_matrix[*index][path[i - 1]])
                    index = j;
            }
        }
        path[i] = *index;
        state = state ^ 1 << path[i];
    }

    return *cost;
}

extern "C" double build_path(const size_t size, double *latitudes, double *longitudes) {
    std::vector<size_t> path(size);
    std::vector<std::vector<double>> distance_matrix = calculate_distance_matrix(size, latitudes, longitudes);
    double cost = solve_tsp(size, distance_matrix, path.data());

    // Reorder latitudes and longitudes according to the path
    std::vector<double> new_latitudes(size), new_longitudes(size);
    for (size_t i = 0; i < size; ++i) {
        new_latitudes[i] = latitudes[path[i]];
        new_longitudes[i] = longitudes[path[i]];
    }

    // Copy the new values back to the original latitudes/longitudes
    std::copy(new_latitudes.begin(), new_latitudes.end(), latitudes);
    std::copy(new_longitudes.begin(), new_longitudes.end(), longitudes);

    return cost;
}
