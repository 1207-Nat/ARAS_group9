#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
UART Device Diagnostic for C4001 Radar Sensor
Finds the correct serial port for your Raspberry Pi
'''

import os
import serial

print("="*60)
print("UART Device Diagnostic for C4001 Radar Sensor")
print("="*60)

# Test 1: Check for UART devices
print("\n[Test 1] Scanning for UART devices...")
uart_devices = []

# Check common UART ports
common_ports = ['/dev/ttyAMA0', '/dev/ttyS0', '/dev/ttyUSB0', '/dev/ttyACM0']

for port in common_ports:
    if os.path.exists(port):
        uart_devices.append(port)
        print(f"✓ Found: {port}")

if not uart_devices:
    print("✗ No UART devices found")
    print("\n  To enable UART on Raspberry Pi:")
    print("  1. Run: sudo raspi-config")
    print("  2. Go to: Interface Options → Serial Port")
    print("  3. Select: YES (enable serial port hardware)")
    print("  4. Reboot: sudo reboot")
else:
    print(f"\nAvailable UART devices: {', '.join(uart_devices)}")

# Test 2: Check if we can open UART
if uart_devices:
    print(f"\n[Test 2] Testing UART connection on {uart_devices[0]}...")
    try:
        ser = serial.Serial(uart_devices[0], baudrate=9600, timeout=1)
        print(f"✓ Successfully opened {uart_devices[0]}")
        print(f"  Baudrate: 9600")
        print(f"  Status: Ready for communication")
        ser.close()
    except Exception as e:
        print(f"✗ Could not open {uart_devices[0]}: {e}")

print("\n[Test 3] Hardware Connection Checklist:")
print("  ☐ Sensor TX connected to Raspberry Pi RXD (GPIO 15, physical pin 10)")
print("  ☐ Sensor RX connected to Raspberry Pi TXD (GPIO 14, physical pin 8)")
print("  ☐ Sensor GND connected to Raspberry Pi GND (pins 6, 9, 14, 20, 25, 30, 34, 39)")
print("  ☐ Sensor VCC connected to 5V or 3.3V power")
print("  ☐ UART is enabled in raspi-config")

print("\n" + "="*60)
print("Diagnostic Complete")
print("="*60)

if uart_devices:
    print(f"\nUpdate your code to use: {uart_devices[0]}")
