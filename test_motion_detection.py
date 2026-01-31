#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
C4001 Motion Detection Test
Tests if the sensor can detect motion
'''

from __future__ import print_function
import sys
import os
sys.path.append("../")
import time
from RADAR_Library import *

print("="*60)
print("C4001 Motion Detection Test")
print("="*60)

# Initialize sensor in UART mode
print("\n[1] Initializing sensor...")
radar = DFRobot_C4001_UART(9600)

if not radar.begin():
    print("✗ Sensor initialization failed!")
    sys.exit(1)

print("✓ Sensor initialized")
time.sleep(1)

# Set to EXIST mode (motion detection mode)
print("\n[2] Setting to EXIST_MODE (motion detection)...")
radar.set_sensor_mode(EXIST_MODE)
time.sleep(2)

# Set very low sensitivity to make detection easier
print("\n[3] Setting sensitivity to minimum (0) for easier detection...")
radar.set_trig_sensitivity(0)
radar.set_keep_sensitivity(0)
time.sleep(1)

# Set simple detection range
print("\n[4] Setting detection range (30-2000cm)...")
radar.set_detection_range(30, 2000, 100)
time.sleep(1)

print("\n[5] Starting motion detection test...")
print("    Move your hand in front of the sensor!")
print("-"*60)

no_motion_count = 0
motion_count = 0

for i in range(30):  # Test for 30 seconds
    motion = radar.motion_detection()
    
    if motion == 1:
        print(f"[{i}s] ✓ MOTION DETECTED")
        motion_count += 1
        no_motion_count = 0
    else:
        print(f"[{i}s] - No motion")
        no_motion_count += 1
    
    time.sleep(1)

print("-"*60)
print(f"\nResults:")
print(f"  Motion detected: {motion_count} times")
print(f"  No motion: {no_motion_count} times")

if motion_count > 0:
    print("\n✓ Sensor is working! Motion detection successful.")
else:
    print("\n✗ No motion detected.")
    print("\nTroubleshooting steps:")
    print("  1. Verify TX/RX wires are connected correctly")
    print("  2. Check if sensor is powered on")
    print("  3. Try moving object directly in front of sensor (within 1m)")
    print("  4. Verify baud rate is 9600")
    print("  5. Check sensor documentation for detection range limits")

print("\n" + "="*60)
