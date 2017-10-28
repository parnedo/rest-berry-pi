# rest-berry-pi
Rest interface to control the raspberry pi


Here you have a generic rest based web server to control your raspberry pi.

# Setup
First let's configure our raspberry to connect to a wifi.

Let's configure wpa\_supplicant 
```
cat /etc/wpa_supplicant/wpa_supplicant.conf 
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
	ssid="ESSID"
	scan_ssid=1
	key_mgmt=WPA-PSK
	psk="PASSWORD"
}

```

# install

Now let's install the environment needed to run the web server

```
sudo apt-get install virtualenv python-dev screen git 
git clone https://github.com/parnedo/rest-berry-pi.git
cd rest-berry-pi
virtualenv venv
source venv/bin/activate
pip install  -r setup/requirements.txt 
```
