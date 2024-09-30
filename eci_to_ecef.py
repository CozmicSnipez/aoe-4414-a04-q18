# eci_to_ecef.py
#
# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
# Converts ECI (Earth-Centered Inertial) coordinates to ECEF (Earth-Centered Earth-Fixed) coordinates
# Parameters:
#  year: The year as an integer
#  month: The month as an integer (1-12)
#  day: The day as an integer (1-31)
#  hour: The hour as an integer (0-23)
#  minute: The minute as an integer (0-59)
#  second: The second as a float (can include a decimal portion)
#  eci_x_km: The ECI X-coordinate in kilometers
#  eci_y_km: The ECI Y-coordinate in kilometers
#  eci_z_km: The ECI Z-coordinate in kilometers
# Output:
#  Prints the ECEF x, y, and z coordinates in km
#
# Written by Nick Davis
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# Import necessary modules
import math
import sys
from datetime import datetime, timedelta
from math import pi, fmod

# Constants
OMEGA_EARTH = 7.292115*10**-5  # Earth's rotation rate in radians per second

# Helper function to calculate fractional Julian date
def ymdhms_to_jd(year, month, day, hour, minute, second):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    frac_day = (hour + minute / 60.0 + second / 3600.0) / 24.0
    return jd + frac_day

# Helper function to calculate the Greenwich Sidereal Time (GST) in radians
def gst_from_jd(jd):  
    T = (jd-2451545.0)/36525
    GMST_seconds = 67310.54841 + (876600*60*60 + 8640184.812866)*T+ 0.093104*T**2- 6.2e-6 * T**3 # ouput in seconds? 
    gst_rad = fmod(GMST_seconds%86400 * OMEGA_EARTH + 2*pi, 2*pi)
    return gst_rad

# Function to convert ECI to ECEF
def eci_to_ecef(jd, eci_x_km, eci_y_km, eci_z_km):
    gst_rad = -gst_from_jd(jd)
    gst_radClass = -0.523603
    cos_gst = math.cos(gst_rad)
    sin_gst = math.sin(gst_rad)

    #print(gst_radClass)
    #print(gst_rad)
    
    ecef_x_km = eci_x_km*cos_gst-eci_y_km*sin_gst
    ecef_y_km = eci_y_km*cos_gst+eci_x_km*sin_gst
    ecef_z_km = eci_z_km
    return ecef_x_km, ecef_y_km, ecef_z_km

# Parse script arguments
if len(sys.argv) == 10:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    eci_x_km = float(sys.argv[7])
    eci_y_km = float(sys.argv[8])
    eci_z_km = float(sys.argv[9])
else:
    print('Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km')
    exit()

# Calculate the Julian Date
jd = ymdhms_to_jd(year, month, day, hour, minute, second)

# Convert ECI to ECEF
ecef_x_km, ecef_y_km, ecef_z_km = eci_to_ecef(jd, eci_x_km, eci_y_km, eci_z_km)

# Print ECEF coordinates in km
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)
