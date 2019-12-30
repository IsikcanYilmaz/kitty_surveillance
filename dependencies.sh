
sudo apt-get update

# PyQt5
echo "[*] Installing PyQt5"
# pip3 install PyQt5

# pigpio
# git clone https://github.com/joan2937/pigpio
echo "[*] Installing pigpio"
sudo apt-get install pigpio
pip3 install pigpio

# Set up pigpiod service to be run on startup
echo "[!] You may want to set up pigpiod to run at startup."
echp "To do that, consider adding pigpiod to /etc/rc.local"
