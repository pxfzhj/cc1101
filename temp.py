f"\rCurrent: {rssi} dB / Min: {min_rssi} dB / Max: {max_rssi} dB"
修改为：
"\rCurrent: {rssi} dB / Min: {min_rssi} dB / Max: {max_rssi} dB".format(rssi=rssi, min_rssi=min_rssi, max_rssi=max_rssi)
