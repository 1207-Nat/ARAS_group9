# Dual Radar Setup Guide for Raspberry Pi

## Hardware Setup

### Radar 1 Configuration
- **TX Pin**: GPIO 14 (default UART TX)
- **RX Pin**: GPIO 15 (default UART RX)
- **Serial Port**: `/dev/ttyAMA0`
- **Baud Rate**: 9600

### Radar 2 Configuration
- **TX Pin**: GPIO 16 (secondary UART TX)
- **RX Pin**: GPIO 20 (secondary UART RX)
- **Serial Port**: `/dev/ttyS0`
- **Baud Rate**: 9600

## Wiring Guide

### Radar 1 (Default UART - ttyAMA0)
```
Radar TX -> Raspberry Pi GPIO 15 (RXD)
Radar RX -> Raspberry Pi GPIO 14 (TXD)
Radar GND -> Raspberry Pi GND
```

### Radar 2 (Secondary UART - ttyS0)
```
Radar TX -> Raspberry Pi GPIO 16 (TX1)
Radar RX -> Raspberry Pi GPIO 20 (RX1)
Radar GND -> Raspberry Pi GND
```

## Software Configuration

### Step 1: Enable Secondary UART
Edit the boot configuration file:
```bash
sudo nano /boot/config.txt
```

Add or uncomment the following lines at the end of the file:
```
# Enable primary UART (GPIO 14/15)
enable_uart=1

# Enable secondary UART on GPIO 16/20 (UART1)
dtoverlay=uart1,txd1_pin=16,rxd1_pin=20

# Optional: Disable shell output on UART
dtoverlay=disable-bt
```

### Step 2: Save and Reboot
Press `Ctrl+X`, then `Y`, then `Enter` to save.

Reboot your Raspberry Pi:
```bash
sudo reboot
```

### Step 3: Verify UART Interface
After reboot, check that both serial ports are available:
```bash
ls -la /dev/ttyAMA0 /dev/ttyS0
```

You should see both interfaces listed.

### Step 4: Install Python Serial Library (if not already installed)
```bash
pip install pyserial
```

## Running the Dual Radar Script

Navigate to your project directory and run:
```bash
python3 DEMO_DUAL_RADAR.py
```

The output should show data from both radars in real-time:
```
=====================================
   Dual Radar System Initialization  
=====================================

Setting up Radar 1 (/dev/ttyAMA0)...
UART initialized on port /dev/ttyAMA0 with baud 9600

=== Radar 1 Configuration ===
Min range: 30 cm
Max range: 2000 cm
Threshold: 20
...
```

## Troubleshooting

### Problem: `/dev/ttyS0` not found
**Solution**: 
- Verify the configuration in `/boot/config.txt`
- Reboot the system
- Check with: `sudo cat /proc/device-tree/aliases | grep -a serial`

### Problem: Permission denied when accessing serial ports
**Solution**:
```bash
sudo usermod -a -G dialout $USER
sudo usermod -a -G gpio $USER
# Then log out and log back in
```

### Problem: Device busy error
**Solution**:
- Make sure no other process is using the serial port
- Check: `lsof /dev/ttyAMA0` and `lsof /dev/ttyS0`
- Kill any interfering processes

### Problem: No data from one or both radars
**Solution**:
1. Verify physical wiring connections
2. Test each radar individually using DEMO_RADARC4001.py with the correct port
3. Check baud rate matches (should be 9600)
4. Use a USB serial adapter to test the radar independently

## Alternative: Using USB-to-Serial Adapter

If GPIO 16/20 secondary UART doesn't work, you can use a USB-to-Serial adapter:
```bash
# Find the device
ls /dev/ttyUSB*
```

Then modify DEMO_DUAL_RADAR.py to use:
```python
radar2 = DFRobot_C4001_UART(9600, port="/dev/ttyUSB0")
```

## Testing Individual Radars

To test each radar separately, you can modify DEMO_RADARC4001.py:

For Radar 1 (default):
```python
radar = DFRobot_C4001_UART(9600)  # Uses /dev/ttyAMA0
```

For Radar 2:
```python
radar = DFRobot_C4001_UART(9600, port="/dev/ttyS0")
```

## Optional: Capture Data to File

Modify DEMO_DUAL_RADAR.py to log data:
```python
with open('radar_data.csv', 'a') as f:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    f.write(f"{timestamp},{radar1_data['speed']},{radar1_data['range']},"
            f"{radar2_data['speed']},{radar2_data['range']}\n")
```

## References

- [Raspberry Pi UART Documentation](https://www.raspberrypi.com/documentation/computers/configuration.html#enable-serial-port)
- [DFRobot C4001 Radar Documentation](https://github.com/DFRobot/DFRobot_C4001)
