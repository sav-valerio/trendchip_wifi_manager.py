# trendchip_wifi_manager.py

**This project doesn't work on Python 2.x.**

**trendchip_wifi_manager.py** is a simple script&mdash;written in Python&mdash; that simplify turning on and off the Wi-Fi module on a Trendchip based access point, without any user interaction.

## What's it?

Usually, Trendchip-based access points don't have any internal scheduling, so I wrote my own :kissing_heart:

You should consider pairing it with a _job scheduler_, in order to automate the process even more.

I've included all the **systemd** units and timers that you could use (and edit, depending on your needs).
If you [hate systemd](http://without-systemd.org/wiki/index.php/Main_Page)&mdash;or your distribution doesn't use it&mdash;you can use whatever [cron implementation](https://wiki.archlinux.org/index.php/cron) you like.

## Installation

Currently, you can't fetch it from **PyPI** but you have to clone this repository and install the dependencies manually.

```shell
git clone https://github.com/sav-valerio/trendchip_wifi_manager.py
cd "trendchip_wifi_manager.py/"
pip install -r requirements.txt
```

If you did change the web interface's password (something **you HAVE to do for safety purposes**)
or if your _access point_ address is different from the default one (`192.168.1.1`), then edit the script accordingly.

## Requirements
You need an always-on server **connected via Ethernet** that will run the script, such as a Raspberry Pi or anything running GNU/Linux on it.

As far as I know, various TP-LINK (such as my TD-W8951ND and TD-W8151N) and Techmade routers/access points are compatible with the script. If you had the chance to try it out on some other devices, let me know through a PR.

Usually, if the web interface is like this, it's likely that the script will work just fine:

![Trendchip web interface](https://raw.githubusercontent.com/sav-valerio/trendchip_wifi_manager.py/master/web_interface.jpg)

## Usage

First, check if you need to tweak some configuration options, in order to make the script work:

```sh
$ nano trendchip_wifi_manager.py
...
host = 192.168.1.1
password = admin
...
```

If you're on _systemd_: you have to edit the unit files, in order to point to the correct script path:

```sh
$ cd systemd
$ nano trendchip_wifi_enable.service
ExecStart=/opt/wifi_scripts/trendchip_wifi_manager.py -e
$ nano trendchip_wifi_disable.service
ExecStart=/opt/wifi_scripts/trendchip_wifi_manager.py -d
```

After editing the unit files, you can work on the timers.
For more information about `OnCalendar` syntax see [systemd.time(7)](http://man7.org/linux/man-pages/man7/systemd.time.7.html).

```sh
$ nano trendchip_wifi_enable.timer
OnCalendar=*-*-* 6:30:00
$ nano trendchip_wifi_disable.timer
OnCalendar=*-*-* 1:00:00
```

Finally, you have to install the unit files and activate the timers.

```sh
$ sudo cp * /etc/systemd/system
$ sudo systemctl daemon-reload
$ sudo systemctl start wifi_enable.timer
$ sudo systemctl start wifi_disable.timer
```

## License
The source code in this repository is licensed under [GNU General Public Licence 3.0](LICENSE).

