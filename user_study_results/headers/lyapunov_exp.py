import numpy as np
from scipy.spatial.distance import pdist, squareform

def lyapunov_exponent(time_series, epsilon=0.001, max_iterations=1000):
    """
    Compute the Lyapunov exponent of a time series.
    
    Parameters:
    - time_series: list or np.array, the time series data
    - epsilon: float, small perturbation to compute divergence
    - max_iterations: int, maximum number of iterations for the computation
    
    Returns:
    - lyapunov_exponent: float, the computed Lyapunov exponent
    """
    n = len(time_series)
    if n < 2:
        raise ValueError("Time series is too short to compute Lyapunov exponent.")
    
    # Create an array to store the divergences
    divergences = np.zeros(max_iterations)
    
    for i in range(1, max_iterations):
        # Select two nearby points in the time series
        j = (i + 1) % n
        if j == 0: break
        x_i, x_j = time_series[i], time_series[j]
        
        # Compute the initial distance
        delta_0 = abs(x_i - x_j)
        if delta_0 < epsilon:
            continue
        
        # Iterate through the time series and compute the divergence
        for k in range(1, n - i):
            x_i_k = time_series[i + k] if (i + k) < n else time_series[(i + k) % n]
            x_j_k = time_series[j + k] if (j + k) < n else time_series[(j + k) % n]
            delta_k = abs(x_i_k - x_j_k)
            divergences[k] += np.log(delta_k / delta_0)
    
    # Average the divergences and compute the Lyapunov exponent
    divergences = divergences[divergences != 0] / (n - 1)
    return np.mean(divergences)

def compare_time_series(ts1, ts2, epsilon=0.001, max_iterations=1000):
    """
    Compare the variability and similarity of two time series using the Lyapunov exponent.
    
    Parameters:
    - ts1: list or np.array, the first time series data
    - ts2: list or np.array, the second time series data
    - epsilon: float, small perturbation to compute divergence
    - max_iterations: int, maximum number of iterations for the computation
    
    Returns:
    - lyapunov_ts1: float, Lyapunov exponent of the first time series
    - lyapunov_ts2: float, Lyapunov exponent of the second time series
    - similarity: float, similarity score based on Lyapunov exponents
    """
    lyapunov_ts1 = lyapunov_exponent(ts1, epsilon, max_iterations)
    lyapunov_ts2 = lyapunov_exponent(ts2, epsilon, max_iterations)
    
    # Compute similarity (higher similarity score means more similar time series)
    similarity = 1 / (1 + abs(lyapunov_ts1 - lyapunov_ts2))
    
    return lyapunov_ts1, lyapunov_ts2, similarity

# Example usage
ts1 = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4]
ts2 = [0.1, 0.2, 0.5, 0.9, 1.5, 3.0, 6.0]

lyapunov_ts1, lyapunov_ts2, similarity = compare_time_series(ts1, ts2)
print(f"Lyapunov exponent of time series 1: {lyapunov_ts1}")
print(f"Lyapunov exponent of time series 2: {lyapunov_ts2}")
print(f"Similarity between time series: {similarity}")
