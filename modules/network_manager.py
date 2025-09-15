import psutil

class NetworkManager:
    def __init__(self):
        self._interfaces = self._load_interfaces()

    def _load_interfaces(self):
        interfaces = {}
        interface_stats = psutil.net_if_stats()
        interface_addrs = psutil.net_if_addrs()

        for name, stats in interface_stats.items():
            addrs = interface_addrs.get(name, [])
            interfaces[name] = NetworkInterface(
                name=name,
                addrs=addrs,
                is_up=stats.isup
            )
        return interfaces

    def list_interfaces(self):
        """Returns a list of all network interface names."""
        return list(self._interfaces.keys())

    def get_interface(self, name):
        """
        Returns a NetworkInterface object for a given name, or None if not found.
        """
        return self._interfaces.get(name)

    def get_all_interfaces_info(self):
        """Returns a list of dictionaries with info for all interfaces."""
        return [iface.get_info() for iface in self._interfaces.values()]

    def get_active_interfaces(self):
        """Returns a list of NetworkInterface objects that are currently up."""
        return [iface for iface in self._interfaces.values() if iface.is_up]

# Example Usage
if __name__ == "__main__":
    try:
        manager = NetworkManager()
        
        # Get information for all interfaces
        all_interfaces = manager.get_all_interfaces_info()
        print("All Interfaces:")
        for iface_info in all_interfaces:
            print(f"- Name: {iface_info['name']}")
            print(f"  Status: {iface_info['status']}")
            print(f"  MAC: {iface_info['mac_address']}")
            print(f"  IPs: {iface_info['ip_addresses']}")
            print("-" * 20)
        
        # Get a specific interface
        specific_iface_name = manager.list_interfaces()[0]
        iface = manager.get_interface(specific_iface_name)
        if iface:
            print(f"\nInformation for {specific_iface_name}:")
            print(iface.get_info())

    except Exception as e:
        print(f"An error occurred: {e}")
        print("This script requires the 'psutil' library. Install it with: pip install psutil")