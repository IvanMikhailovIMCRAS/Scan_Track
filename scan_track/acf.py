import numpy as np

def get_acf(vec: np.ndarray, frac: float = 0.05) -> np.array:
    """Calculatinf AutoCorrelation Function (ACF)

    Args:
        vec (np.ndarray): input vector
        frac (float, optional): fraction of length to analyse. Defaults to 0.05.

    Returns:
        np.array: autocorrelation function
    """
    N = len(vec)
    Nt = int(N * frac)
    if Nt < 1 or Nt > N - 1:
        raise ValueError("Invalid value of frac was used")
    acf = np.zeros(Nt+1, dtype=float)
    for i in range(N- 2 * Nt + 1):
        for j in range(Nt + 1):
            acf[j] += np.sum(vec[i:i+Nt] * vec[i+j:i+j+Nt]) 
    acf0 = acf[0]
    return acf / acf0