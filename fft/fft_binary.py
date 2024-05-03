import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq, irfft
from math import floor

SAMPLE_RATE = 44100  # Hertz
DURATION = 10  # Seconds
TOTAL_POINTS = 1000


def generate_binary_signal(duration):
    # x = list(range(0, duration))
    x = np.linspace(0, duration, TOTAL_POINTS, endpoint=False)
    y = [floor(l)%2 for l in x]
    return x, y


# Generate a sample binary signal
x, y = generate_binary_signal(DURATION)
plt.plot(x, y)
plt.show()

yf = rfft(y)
xf = rfftfreq(TOTAL_POINTS, TOTAL_POINTS/DURATION)

plt.plot(xf, np.abs(yf))
plt.show()

# now, take some harmonics away
yf[TOTAL_POINTS//10:TOTAL_POINTS] = 0
plt.plot(xf, np.abs(yf))
plt.show()

# and now, recover the original signal
# with the inverse FFT
new_y = irfft(yf)
plt.plot(new_y)
plt.show()

# now take all harmonics but the first ones away
yf[10:TOTAL_POINTS] = 0
plt.plot(xf, np.abs(yf))
plt.show()

new_y = irfft(yf)
plt.plot(new_y)
plt.show()
