#!/usr/bin/env python3
# hasscleanup - Home Assistant Cleanup Tool - Remove Devices & Entities
# (c) jamespo [at] gmail [dot] com 2021

import json
import os
import os.path
import sys
import time
from shutil import copyfile
from optparse import OptionParser

debug = False  # global debug flag


class HassCleanup():
    def __init__(self):
        """
        initialized HA cleanup object
        """
        self.opts = None
        self.conffiles = ('core.device_registry', 'core.entity_registry')
        self.parsed_registry = {}

    @staticmethod
    def die(errmsg):
        '''Quit ungracefully'''
        print('Quitting: %s' % errmsg)
        sys.exit(1)

    def parse(self):
        '''parse the core conffiles'''
        for conffile in self.conffiles:
            with open(conffile) as cf:
                self.parsed_registry[conffile] = json.loads(cf.read())

    def remove(self):
        '''remove entities or devices from registries'''
        devices = self.parsed_registry['core.device_registry']['data']['devices']
        entities = self.parsed_registry['core.entity_registry']['data']['entities']
        devids = self.find_ids(devices, self.opts.deviceid, 'id', True)
        entids = self.find_ids(entities, self.opts.deviceid, 'device_id', False)
        ents_removed = self.remove_ids(entities, entids, 'Entities')
        devs_removed = self.remove_ids(devices, devids, 'Devices')
        return ents_removed, devs_removed

    @staticmethod
    def find_ids(items, match, identifier, find_one=True):
        '''find entities or devices in JSON'''
        idxs_found = []
        for idx, item in enumerate(items):
            if match == item[identifier]:
                idxs_found.append(idx)
                if find_one:
                    break
        if debug:
            print("idxs_found: %s" % idxs_found)
        return idxs_found

    @staticmethod
    def remove_ids(items, idxs, label):
        '''remove ids from items'''
        num_removed = 0
        # reverse list so removing earlier doesn't affect position
        for idx in idxs[::-1]:
            items.pop(idx)
            num_removed += 1
            if debug:
                print('Removing %s from %s' % (idx, label))
        return num_removed

    def get_cli_options(self):
        '''get command line options & return OptionParser'''
        global debug
        parser = OptionParser()
        parser.add_option("-d", dest="directory", help=".storage dir location",
                          default=os.getcwd())
        parser.add_option("-i", dest="deviceid", help="deviceid to delete")
        parser.add_option("-n", "--dryrun", dest="dryrun", action="store_true",
                          help="dry run - don't write to files", default=False)
        parser.add_option("--debug", help="turn on debug",
                          dest="debug", action="store_true", default=False)
        parser.add_option("-s", "--skip-backup", dest="backup", action="store_false",
                          help="Skip backup (DANGER)", default=True)
        self.opts, args = parser.parse_args()
        debug = self.opts.debug

    def validate_opts(self):
        '''check cli args'''
        try:
            os.chdir(self.opts.directory)
        except FileNotFoundError:
            self.die("Can't find dir %s" % self.opts.directory)
        if not all((os.path.isfile(conffile) for conffile in self.conffiles)):
            self.die("Can't find conffiles")

    def backup_conf(self):
        '''backup conf'''
        ext = int(time.time())
        for conffile in self.conffiles:
            # already in correct dir from validate_opts
            copyfile(conffile, '%s.%s.bak' % (conffile, ext))

    def writeconf(self, conf):
        '''save cleaned up conf'''
        if debug:
            print(json.dumps(self.parsed_registry[conf], indent=4))
        with open(conf, 'w') as cf:
            cf.write(json.dumps(self.parsed_registry[conf], indent=4))


def main():
    '''get options, do checks, return results'''
    hc = HassCleanup()
    hc.get_cli_options()
    hc.validate_opts()
    if hc.opts.backup:
        hc.backup_conf()
    hc.parse()
    ents_removed, devs_removed = hc.remove()
    if (ents_removed + devs_removed == 0):
        print("Device ID %s not found. Not writing to disk" % hc.opts.deviceid)
    elif not hc.opts.dryrun:
        if ents_removed:
            hc.writeconf('core.entity_registry')
        if devs_removed:
            hc.writeconf('core.device_registry')
        print("Device ID %s removed from %s device and %s entities" %
              (hc.opts.deviceid, devs_removed, ents_removed))
    else:
        print("Dry run - no changes to conf.")


if __name__ == '__main__':
    main()
