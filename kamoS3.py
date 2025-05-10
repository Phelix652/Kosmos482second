import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from skyfield.api import load, EarthSatellite
from datetime import datetime

# Streamlit config
st.set_page_config(layout="wide")
st.title("🌍 Live Satellite Tracker")
st.markdown("Tracking **Kosmos 482** Satellite")

# Estimated reentry site coordinates (Indian Ocean, near Indonesia)
crash_lat = -8.5
crash_lon = 102.0
st.markdown(f"📍 **Final Position (Est.):** Lat: `{crash_lat:.2f}°`, Lon: `{crash_lon:.2f}°`")

my_lat = 16.8409
my_lon = 96.1735

# Kosmos 482 TLE data (hardcoded)
name_kosmos = "Kosmos 482"
tle1_kosmos = "1 06073U 72023B   24123.65777316  .00000803  00000+0  14121-3 0  9990"
tle2_kosmos = "2 06073  51.5533 146.5134 5188798  22.7442 354.1140  5.44340810267680"

# Load time and satellite
ts = load.timescale()

# Kosmos 482 has reentered the atmosphere
crash_time = "2025-05-10 04:20 UTC"

# Set satellite as no longer active
satellite_data_valid = False

# Try to load satellite (will not be used, just for structure)
try:
    sat_kosmos = EarthSatellite(tle1_kosmos, tle2_kosmos, name_kosmos, ts)
except Exception as e:
    pass  # Satellite data is not valid

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
m = Basemap(projection='cyl', resolution='c')
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='midnightblue')
m.fillcontinents(color='forestgreen', lake_color='darkgreen')
m.drawparallels(np.arange(-90., 91., 30.))
m.drawmeridians(np.arange(-180., 181., 60.))

# Plot user's location
x_my, y_my = m(my_lon, my_lat)
ax.scatter(x_my, y_my, color='white', marker='^', s=60, label="Your Location")

if satellite_data_valid:
    # (This branch is now unused but kept for completeness)
    lat, lon, alt, speed, path_lats, path_lons = get_satellite_data(sat_kosmos, ts)
    path_x, path_y = m(path_lons, path_lats)
    ax.plot(path_x, path_y, linestyle='--', color='lime')
    x, y = m(lon, lat)
    ax.scatter(x, y, color='lime', edgecolor='black', s=100, zorder=5, label=sat_kosmos.name)
    st.markdown(f"**{sat_kosmos.name}** — Lat: `{lat:.2f}°`, Lon: `{lon:.2f}°`, Alt: `{alt:.1f} km`, Speed: `{speed:.2f} km/s`")
else:
    # Show crash message
    ax.text(0.5, 0.5, f"The Satellite has crashed\nAt: {crash_time}",
            color='red', fontsize=20, ha='center', va='center', transform=ax.transAxes)
    
    # Plot estimated crash site
    x_crash, y_crash = m(crash_lon, crash_lat)
    ax.scatter(x_crash, y_crash, color='red', marker='o', s=50, label="Estimated Crash Site")

ax.legend(loc='lower left', fontsize=9)
st.pyplot(fig)

# Reload button
if st.button("🔁 Reload Satellite Data"):
    st.rerun()

st.markdown("Design by Mr Zay Bhone Aung")
