#!/usr/bin/env python3
import subprocess
import time
import re

def run_vcgencmd(command):
    """Run vcgencmd and return output as string."""
    try:
        result = subprocess.run(
            ["vcgencmd"] + command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("vcgencmd not found. Install Raspberry Pi firmware tools.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e}")

def get_voltage():
    """Get core voltage in volts."""
    output = run_vcgencmd("measure_volts")
    match = re.search(r"volt=([\d.]+)V", output)
    return float(match.group(1)) if match else None

def get_current():
    """
    Get current draw in amperes.
    On Pi 5, 'measure_current' may be available for rails like 'core' or 'sdram'.
    """
    try:
        output = run_vcgencmd("measure_current core")
        match = re.search(r"current=([\d.]+)A", output)
        return float(match.group(1)) if match else None
    except RuntimeError:
        return None  # Not supported on all firmware versions

if __name__ == "__main__":
    try:
        while True:
            voltage = get_voltage()
            current = get_current()

            if voltage is not None:
                print(f"Voltage: {voltage:.3f} V")
            else:
                print("Voltage reading not available.")

            if current is not None:
                print(f"Current: {current:.3f} A")
            else:
                print("Current reading not available on this firmware.")

            print("-" * 30)
            time.sleep(2)  # Update every 2 seconds

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
    except RuntimeError as e:
        print(f"Error: {e}")
