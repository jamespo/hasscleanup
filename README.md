# hasscleanup
Home Assistant Cleanup Tool - Remove Devices &amp; Entities

Use this to remove unwanted devices/entities from your Home Assistant install.


Usage
-----

Shut HA down before use.


    hasscleanup.py [options]

    Options:
    -h, --help         show this help message and exit
    -d DIRECTORY       .storage dir location
    -i DEVICEID        deviceid to delete
    -n, --dryrun       dry run - don't write to files
    --debug            turn on debug
    -s, --skip-backup  Skip backup (DANGER)

To get the DEVICEID, go to Configuration -> Devices & select the device in the web UI.

The URL will look like http://YOUR.HA.IP:8123/config/devices/device/e45b71334133d6e5ae6f9fb5dc9eaa86

The long hex string is the DEVICEID.

If you want to remove this from your conf, and the GUI doesn't give you the option (I've found this with SmartThings devices for example) you would use the tool.

cd into your homeassistant .storage directory (below your conf files) and run:

     hasscleanup.py -i e45b71334133d6e5ae6f9fb5dc9eaa86

It will make a backup and cleanup the core.device_registry & core.entity_registry conf files.

Now restart HA & test.
