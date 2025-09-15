import cmd
import shlex
import sys
import os
import json

class AdminShell(cmd.Cmd):
    """
    An interactive shell for a system's admin user interface.
    It can operate both online and offline.
    """
    intro = 'Welcome to the Admin Shell. Type help or ? to list commands.\n'
    prompt = '(admin) $ '

    def __init__(self, is_online=True):
        super().__init__()
        self.is_online = is_online
        self.offline_mode_data = {}  # Data stored for offline manipulation

    def precmd(self, line):
        """Hook to be executed before a command is dispatched."""
        # A simple check to show online/offline status
        if not self.is_online:
            print("You are in offline mode. Changes will be saved locally.")
        return line

    def do_status(self, line):
        """
        Check the current connection status.
        Usage: status
        """
        if self.is_online:
            print("System is currently ONLINE.")
        else:
            print("System is currently OFFLINE.")
    
    def do_go_offline(self, line):
        """
        Switch the shell to offline mode.
        Usage: go_offline
        """
        self.is_online = False
        print("Switched to offline mode. All commands will now operate on local data.")
        
    def do_go_online(self, line):
        """
        Switch the shell to online mode.
        Usage: go_online
        """
        self.is_online = True
        print("Switched to online mode. Will attempt to sync local changes.")
        # In a real system, you would add logic to sync self.offline_mode_data to the main database
        
    def do_exit(self, line):
        """
        Exit the admin shell.
        Usage: exit
        """
        print("Exiting Admin Shell.")
        return True # Returning True exits the command loop
    
    def do_quit(self, line):
        """
        Exit the admin shell.
        Usage: quit
        """
        return self.do_exit(line)

    def do_show_data(self, line):
        """
        Display current local or remote data.
        Usage: show_data
        """
        if self.is_online:
            # Placeholder for online functionality
            print("--- ONLINE DATA ---")
            print("Fetching data from remote server...")
            # Example: data = fetch_from_api()
        else:
            print("--- OFFLINE DATA ---")
            print(json.dumps(self.offline_mode_data, indent=2))

    def do_add_entry(self, line):
        """
        Add a new entry to the system.
        Usage: add_entry <key> <value>
        """
        try:
            key, value = shlex.split(line)
            if self.is_online:
                print(f"Attempting to add '{key}':'{value}' to the live system...")
                # Real-world: api.add_entry(key, value)
                print("Online update successful!")
            else:
                self.offline_mode_data[key] = value
                print(f"Added '{key}':'{value}' to offline data.")
        except ValueError:
            print("Invalid command format. Use: add_entry <key> <value>")

    def do_save_offline(self, line):
        """
        Save the current offline data to a file.
        Usage: save_offline <filename>
        """
        if not line:
            print("Please provide a filename. Usage: save_offline <filename>")
            return
        
        filename = line
        try:
            with open(filename, 'w') as f:
                json.dump(self.offline_mode_data, f, indent=2)
            print(f"Offline data saved to '{filename}'.")
        except Exception as e:
            print(f"Error saving file: {e}")

# Entry point for the application
if __name__ == '__main__':
    # Determine the initial mode
    initial_mode = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == '--offline':
        initial_mode = False

    shell = AdminShell(is_online=initial_mode)
    shell.cmdloop()