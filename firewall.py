import tkinter as tk
from tkinter import messagebox
import subprocess
import logging
import re
import ctypes
import sys  # Import missing sys module

# Setup the logging
logging.basicConfig(filename='firewall.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to check for admin rights
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class AdvancedFirewallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Firewall Simulator")

        # Input for IP address or range
        tk.Label(root, text="IP Address/Range:").grid(row=0, column=0)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.grid(row=0, column=1)

        # Block button
        block_button = tk.Button(root, text="Block", command=self.block_action)
        block_button.grid(row=1, column=0, columnspan=2)

        # Unblock button
        unblock_button = tk.Button(root, text="Unblock", command=self.unblock_action)
        unblock_button.grid(row=2, column=0, columnspan=2)

        # View log button
        log_button = tk.Button(root, text="View Log", command=self.view_log)
        log_button.grid(row=3, column=0, columnspan=2)

    def block_action(self):
        ip = self.ip_entry.get()
        if self.validate_ip(ip):
            try:
                # Windows command to block an IP address or range
                subprocess.run(f"netsh advfirewall firewall add rule name=\"BlockIP{ip}\" dir=in action=block remoteip={ip}", shell=True, check=True, stderr=subprocess.PIPE)
                logging.info(f"Blocked IP/Range: {ip}")
                messagebox.showinfo("Success", f"Successfully blocked IP/Range: {ip}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to block IP/Range: {ip}\n{e.stderr.decode().strip()}")
        else:
            messagebox.showerror("Error", "Invalid IP/Range")

    def unblock_action(self):
        ip = self.ip_entry.get()
        if self.validate_ip(ip):
            try:
                # Windows command to unblock an IP address or range
                subprocess.run(f"netsh advfirewall firewall delete rule name=\"BlockIP{ip}\"", shell=True, check=True, stderr=subprocess.PIPE)
                logging.info(f"Unblocked IP/Range: {ip}")
                messagebox.showinfo("Success", f"Successfully unblocked IP/Range: {ip}")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to unblock IP/Range: {ip}\n{e.stderr.decode().strip()}")
        else:
            messagebox.showerror("Error", "Invalid IP/Range")

    def view_log(self):
        # This will show the log contents in a message box
        with open('firewall.log', 'r') as log_file:
            log_contents = log_file.read()
            messagebox.showinfo("Firewall Log", log_contents)

    @staticmethod
    def validate_ip(ip):
        # Regex to validate an IP address or CIDR range
        pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$")
        return pattern.match(ip) is not None

if __name__ == "__main__":
    if is_admin():
        root = tk.Tk()
        app = AdvancedFirewallApp(root)
        root.mainloop()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
