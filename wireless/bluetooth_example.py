#
# Bluetooth example using the PyBluez library.
# Requires Windows SDK: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
# 
# PyBluez installation:
#   git clone https://github.com/pybluez/pybluez
#   cd pybluez
#   python -m venv venv
#   .\venv\Scripts\activate.ps1
#   pip install wheel
#   python setup.py install
#   python setup.py bdist_wheel
#   .\venv\Scripts\deactivate.bat
#
# Go to networking_examples folder and activate your venv
#    pip install ..\pybluez\dist\PyBluez-0.22-cp36-cp36m-win_amd64.whl
# 

import bluetooth

nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

print("Found {} devices".format(len(nearby_devices)))

for addr, name in nearby_devices:
    try:
        print("   {} - {}".format(addr, name))
        services = bluetooth.find_service(address=addr)

        if len(services) > 0:
            print("Found {} services on {}.".format(len(services), name))
        else:
            print("No services found.")

        for svc in services:
            print("\nService Name:", svc["name"])
            print("    Host:       ", svc["host"])
            print("    Description:", svc["description"])
            print("    Provided By:", svc["provider"])
            print("    Protocol:   ", svc["protocol"])
            print("    channel/PSM:", svc["port"])
            print("    svc classes:", svc["service-classes"])
            print("    profiles:   ", svc["profiles"])
            print("    service id: ", svc["service-id"])

    except UnicodeEncodeError:
        print("   {} - {}".format(addr, name.encode("utf-8", "replace")))

