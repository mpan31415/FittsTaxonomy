import numpy as np

def sample_entropy(time_series, m=2, r=0.2):
    """
    Compute the sample entropy of a time series.
    
    Parameters:
    - time_series: list or np.array, the time series data
    - m: int, length of sequences to be compared
    - r: float, tolerance for accepting matches (typically 0.2 * standard deviation of the time series)
    
    Returns:
    - sample_entropy: float, the computed sample entropy
    """
    N = len(time_series)
    if N <= m + 1:
        raise ValueError("Time series is too short to compute sample entropy.")
    
    # Standard deviation of the time series
    std_time_series = np.std(time_series)
    
    # Compute the number of matches for m-length and (m+1)-length sequences
    def _phi(m):
        x = np.array([time_series[i:i + m] for i in range(N - m)])
        C = np.sum(np.max(np.abs(x[:, None] - x[None, :]), axis=2) <= r * std_time_series, axis=0) / (N - m)
        return np.sum(np.log(C)) / (N - m)
    
    return _phi(m) - _phi(m + 1)

# Example usage
time_series1 = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4]
time_series2 = [0.1, 0.2, 0.5, 0.9, 1.5, 3.0, 6.0, 0.1, 0.2, 0.5, 0.9, 1.5, 3.0, 6.0]

se1 = sample_entropy(time_series1)
se2 = sample_entropy(time_series2)

print(f"Sample entropy of time series 1: {se1}")
print(f"Sample entropy of time series 2: {se2}")
