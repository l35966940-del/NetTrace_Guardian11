# main.py - The main entry point for the NetTrace_Guardian security suite.
# This file will be renamed to NetTrace_Guardian.py later.

import os
import importlib.util
import threading
import time

# Define the paths for our modules and utility libraries
MODULES_DIR = "modules"
UTIL_DIR = "util"

class NetTraceGuardian:
    def __init__(self):
        self.modules = {}
        self.active_protections = []
        self.running = True
        self.cli_thread = None

    def _load_modules(self):
        """Loads all Python modules from the modules directory."""
        print("Loading security modules...")
        for filename in os.listdir(MODULES_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                filepath = os.path.join(MODULES_DIR, filename)

                try:
                    spec = importlib.util.spec_from_file_location(module_name, filepath)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'run'):
                        self.modules[module_name] = module
                        print(f"  - Successfully loaded {module_name}")
                    else:
                        print(f"  - Skipping {module_name}: 'run' function not found.")
                        
                except Exception as e:
                    print(f"  - Failed to load module {module_name}: {e}")

    def _cli(self):
        """Simple command-line interface for user interaction."""
        while self.running:
            command = input("NetTrace_Guardian> ").lower().strip()
            if command == "quit":
                self.running = False
            elif command == "list":
                print("Available modules:")
                for name in self.modules.keys():
                    print(f"  - {name}")
            else:
                print("Unknown command. Try 'list' or 'quit'.")
            time.sleep(0.1)

    def start(self):
        """Starts the main security suite and all active modules."""
        self._load_modules()
        print("\nNetTrace_Guardian starting...")
        
        # Start the CLI in a separate thread so it doesn't block the main program.
        self.cli_thread = threading.Thread(target=self._cli)
        self.cli_thread.daemon = True
        self.cli_thread.start()
        
        try:
            while self.running:
                # This is where we would check module status and manage other tasks.
                # For now, we'll just keep the main thread alive.
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down NetTrace_Guardian...")
        finally:
            self.stop()
            
    def stop(self):
        """Stops all running components of the security suite."""
        self.running = False
        print("NetTrace_Guardian stopped.")

if __name__ == "__main__":
    guardian = NetTraceGuardian()
    guardian.start()