#!/bin/sh

crontab -l > /tmp/crontab.tmp
echo "@reboot /home/pi/tsunagaru-kun-device/run.sh" >> /tmp/crontab.tmp

if [crontab -u pi /tmp/crontab.tmp]; then
	echo "linstalling crontab is successfully"
else
	echo "installing crontab is failed"
fi

rm /tmp/crontab.tmp
