#!/usr/bin/python3
# trendchip_wifi_manager.py
# Enable and disable the Wi-Fi module into your Trendchip based access point without any user interaction. Edit
# https://github.com/sav-valerio/trendchip_wifi_manager.py

import sys,getopt,configparser
import telnetlib
import logging
from systemd import journal

config = configparser.ConfigParser()
config['Connection'] = {'HostAddress': '192.168.1.1'}
config['Authentication'] = {'Password' : 'admin'}
with open('config.ini', 'w') as configfile:
	config.write(configfile)

def main(argv):
	try:
		opts,args = getopt.getopt(argv, "ed")

	except getopt.GetoptError:
		print("trendchip_wifi_manager.py [OPTIONS...]")
		print("\n-e --enable     Enable Wi-Fi module")
		print("-d --disable    Disable Wi-Fi module")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print("trendchip_wifi_manager.py [OPTIONS...]")
			print("\n-e --enable     Enable Wi-Fi module")
			print("-d --disable    Disable Wi-Fi module")
			sys.exit()

		elif opt in ("-e", "--enable"):
			tn = telnetlib.Telnet(config['Connection']['HostAddress'])

			tn.read_until(b"Password: ")
			tn.write(config['Authentication']['Password'].encode('ascii') + b"\n")

			tn.write(b"rtwlan enableap\n")
			tn.write(b"exit\n")

			journal.send(MESSAGE='trendchip_wifi_manager.py - Wi-Fi module enabled.')

		elif opt in ("-d", "--disable"):
			tn = telnetlib.Telnet(config['Connection']['HostAddress'])

			tn.read_until(b"Password: ")
			tn.write(config['Authentication']['Password'].encode('ascii') + b"\n")

			tn.write(b"rtwlan disableap\n")
			tn.write(b"exit\n")

			journal.send(MESSAGE='trendchip_wifi_manager.py - Wi-Fi module disabled.')


if __name__ == "__main__":
	main(sys.argv[1:])