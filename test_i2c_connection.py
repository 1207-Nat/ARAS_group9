#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
I2C Connection Diagnostic for C4001 Radar Sensor
Run this script to diagnose I2C connection issues
'''

import sys
import os
sys.path.append("../")
import time

# Test 1: Check if smbus is available
print("="*60)
print("I2C Connection Diagnostic for C4001 Radar Sensor")
print("="*60)

print("\n[Test 1] Checking smbus2 library...")
try:
    import smbus
    print("✓ smbus library is available")
except ImportError:
    print("✗ smbus library not found")
    print("  Install with: sudo apt-get install python3-smbus")
    sys.exit(1)

# Test 2: Check I2C devices
print("\n[Test 2] Scanning I2C bus...")
try:
    import subprocess
    result = subprocess.run(['i2cdetect', '-y', '1'], capture_output=True, text=True)
    print("I2C Device List:")
    print(result.stdout)
    if '2a' in result.stdout.lower() or '2b' in result.stdout.lower():
        print("✓ Found C4001 sensor on I2C bus!")
    else:
        print("⚠ C4001 not found. Possible addresses: 0x2A or 0x2B")
except Exception as e:
    print(f"⚠ Could not run i2cdetect: {e}")
    print("  Install with: sudo apt-get install i2c-tools")

# Test 3: Try to read from the sensor
print("\n[Test 3] Testing direct I2C read at 0x2A...")
try:
    bus = smbus.SMBus(1)
    data = bus.read_i2c_block_data(0x2A, 0x00, 1)
    print(f"✓ Successfully read from 0x2A: {hex(data[0])}")
    print("  Your sensor is responsive!")
except IOError as e:
    print(f"✗ I/O Error at 0x2A: {e}")
    print("\n  Troubleshooting:")
    print("  1. Check power supply to sensor")
    print("  2. Verify SDA (GPIO 2) and SCL (GPIO 3) connections")
    print("  3. Check for loose or damaged wires")
    print("  4. Verify pull-up resistors (4.7kΩ) are present")
    print("  5. Try address 0x2B instead of 0x2A")
    
    # Try 0x2B
    print("\n[Test 3b] Trying alternate address 0x2B...")
    try:
        data = bus.read_i2c_block_data(0x2B, 0x00, 1)
        print(f"✓ Found sensor at 0x2B instead!")
        print("  Update I2C_ADDR to 0x2B in your code")
    except:
        print("✗ No response at 0x2B either")
except Exception as e:
    print(f"✗ Unexpected error: {e}")

# Test 4: Check voltage levels
print("\n[Test 4] Hardware Connection Checklist:")
print("  ☐ Sensor VCC connected to 3.3V or 5V")
print("  ☐ Sensor GND connected to Raspberry Pi GND")
print("  ☐ Sensor SDA connected to GPIO 2 (pin 3)")
print("  ☐ Sensor SCL connected to GPIO 3 (pin 5)")
print("  ☐ Pull-up resistors installed on SDA/SCL (optional but recommended)")
print("  ☐ No loose or damaged wires")

print("\n" + "="*60)
print("Diagnostic Complete")
print("="*60)
