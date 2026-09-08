import os
try:
    for root, dirs, files in os.walk('/sys/bus/usb/devices'):
        if 'idVendor' in files and 'serial' in files:
            with open(os.path.join(root, 'idVendor'), 'r') as f:
                if f.read().strip() == '04e8':
                    with open(os.path.join(root, 'serial'), 'r') as s:
                        print(f"Serial: {s.read().strip()}")
except Exception as e:
    print(f"Error: {e}")
