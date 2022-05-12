
# analyze data to find high points where the drone might be

# Transform the data as follows
# Frequency -> List<Power>

import matplotlib.pyplot as plt
from math import sqrt, pi

MM = 1e6

avg = lambda list: sum(list) / len(list)

NOISE_THRESHOLD = -55
# Compute the averge power, ignoring those below NOISE_THRESHOLD dB.
peak_avgs = lambda _list: avg(list(filter(lambda db: db > NOISE_THRESHOLD, _list)))

C = 3e8
#power = 10 ** (-45 / 10)

gain_r = 1
gain_t = 1


db_to_pr_over_pt = lambda db: 10 ** (db / 10)

dist = lambda power, freq: sqrt((1 / db_to_pr_over_pt(power)) * (C / (4 * pi * freq)) ** 2 * gain_r * gain_t )


freq = 2443 * 1e6
power = -45

print("Distance({}, {}) = {}".format(power, freq, dist(power,freq)))

freq_bin_to_pows = {}

import sys

with open(sys.argv[1]) as f:
	for line in f:
		tokens = line.split(", ")
		timestamp = tokens[0] + ":" + tokens[1]
		base_freq = float(tokens[2])
		delta_freq = float(tokens[4])

		f = base_freq

		for dbs in list(map((lambda s: float(s)), tokens[6:])):
			if f not in freq_bin_to_pows:
				freq_bin_to_pows[f] = []
			freq_bin_to_pows[f].append(dbs)
			f += delta_freq

for freq, powers in freq_bin_to_pows.items():
	if  2442 < freq / 1e6 < 2444 and max(powers) > -40:
		# this is the drone comm freq
		print("Avg above threshold power at {} = {}" .format( freq / 1e6, peak_avgs(powers) ))
	# if 2440 * MM < freq < 2445 * MM and max(powers) > -40:
		plt.plot(powers)
		plt.title(str(freq / MM) + " MHz")
		plt.show()
