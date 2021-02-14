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
