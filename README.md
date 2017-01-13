# trendchip_wifi_manager.py
trendchip_wifi_manager.py is a simple Python3 script concieved for turnining on and off the Wi-Fi module of a Trendchip based access pointm without any user interaction.

#### Why?
Usually, Trendchip based access points don't have any internal scheduling, so I wrote my own. :P
It is meant to be used with a job scheduler in order to avoiding any user interaction, of course.
I already included all the systemd units and timers that you could use (and modify if needed for suiting your needs).
If you [hate systemd](http://without-systemd.org/wiki/index.php/Main_Page), or your distribution doesn't use it, you can use whatever [cron implementation](https://wiki.archlinux.org/index.php/cron) you like.

### Requirements and compatibility
You'll need an always-on server **connected via Ethernet** that'll run the script, such as a Raspberry Pi or anything that can run GNU/Linux on it. :)
AFAIK various TP-LINK (such as my TD-W8951ND and TD-W8151N) and Techmade routers/access points are compatible.

Usually, if the web interface is like this, it's likely that the script works just fine.

![Trendchip web interface](https://s26.postimg.org/np6j5m0e1/Screenshot_20170113_170705.png)

### Installation
trendchip_wifi_manager.py requires Python 3 and the systemd-python libraries (for logging) to run.
If you don't need any logging, or if you don't have systemd, you can just comment the journal related code.

```sh
$ git clone https://github.com/sav-valerio/trendchip_wifi_manager.py
$ pip3 install systemd-python
```

If you did change the web interface's password (a thing that you should have already done for safety purposes) and/or if your access point address is different from the default one (192.168.1.), edit the script accordingly.

```sh
$ nano trendchip_wifi_manager.py
...
host = 192.168.1.1
password = admin
...
```

Now it's the time to edit and install the Systemd related files.
You have to edit both unit files in order to point the correct path to the script in your drive, then you can copy and enable the units.

```sh
$ cd systemd
$ nano trendchip_wifi_enable.service
ExecStart=/opt/wifi_scripts/trendchip_wifi_manager.py -e
$ nano trendchip_wifi_disable.service
ExecStart=/opt/wifi_scripts/trendchip_wifi_manager.py -d
$ sudo cp * /etc/systemd/system
$ sudo systemctl enable trendchip_wifi_enable.service
$ sudo systemctl enable trendchip_wifi_disable.service
```

Last but not least thing is to edit, install and activate the timers, same as as before.
For more information about OnCalendar syntax see [systemd.time(7)](http://man7.org/linux/man-pages/man7/systemd.time.7.html).
```sh
$ nano trendchip_wifi_enable.timer
OnCalendar=*-*-* 6:30:00
$ nano trendchip_wifi_disable.timer
OnCalendar=*-*-* 1:00:00
$ sudo systemctl enable wifi_enable.timer
$ sudo systemctl start wifi_enable.timer
$ sudo systemctl enable wifi_disable.timer
$ sudo systemctl start wifi_disable.timer
```

Done!

### Credits
Thanks to [@domcorvasce](https://github.com/domcorvasce) for helping me fix my bad mistakes.

### License
GNU General Public Licence 3.0


