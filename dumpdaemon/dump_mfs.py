#!/usr/bin/env python
# Script om 802.11 probe request op te slaan in een mysql database
#
# Copyright 2017 Loran Kloeze - loran@ralon.nl
# Licentie: MIT
#
#

import time
import subprocess
import re
import sys
import os
import MySQLdb
import random
import threading

monitor_iface = 'wlan0'
kanaal_wisselen = True

# Deze thread zorgt ervoor dat het kanaal elke 2 seconden wisselt tussen 1 t/m 13
class RandomizeChannelThread(threading.Thread):
    def __init__(self):
        super(RandomizeChannelThread, self).__init__()

    def run(self):
        while True:
            subprocess.call(['iw', 'dev', monitor_iface, 'set', 'channel', str(random.randint(1,13))])
            time.sleep(2)

# Hoewel tcpdump de monitor interface al in monitor mode zet doen we
# dat hier alvast omdat RandomizeChannelThread anders gaat klagen
def prepareInterface():
    subprocess.call(['ifconfig', monitor_iface, 'down'])
    subprocess.call(['iwconfig', monitor_iface, 'mode', 'monitor'])
    subprocess.call(['ifconfig', monitor_iface, 'up'])

def startProbing():    
    db = MySQLdb.connect(host="localhost",user="wifiscan",passwd="wifiscan",db="wifiscanner") 
    cur = db.cursor()

    proc = subprocess.Popen(['tcpdump', '-l', '-I', '-i', monitor_iface, '-e', '-s', '256', 'type', 'mgt', 'subtype', 'probe-req'],stdout=subprocess.PIPE)
    patt = '(-\d+)dBm signal antenna 1.+SA:([0-9a-f]+:[0-9a-f]+:[0-9a-f]+:[0-9a-f]+:[0-9a-f]+:[0-9a-f]+) .+(Probe Request) \((.+)\)'
    while True:
        line = proc.stdout.readline()
        if line != '':
            m = re.search(patt, line)
            if m is not None and len(m.groups()) == 4:
                signaal = m.group(1).rstrip()
                
                mac = m.group(2).rstrip()
                ssid = m.group(4).rstrip()
                tijd = int(time.time())

                # Is deze SSID al bekend?
                cur.execute('SELECT id FROM ssids WHERE ssid = %s;', [ssid])
                db_ssid = cur.fetchone()
                if db_ssid is not None:
                    ssid_id = db_ssid[0]
                else:
                    cur.execute('INSERT INTO ssids (ssid) VALUES (%s)', [ssid])
                    ssid_id = cur.lastrowid


                # Is het mac-adres al bekend?
                cur.execute('SELECT id FROM mobile_stations WHERE mac = %s;', [mac])
                db_mobile_station = cur.fetchone()
                if db_mobile_station is not None:
                    mobile_station_id = db_mobile_station[0]
                else:
                    cur.execute('INSERT INTO mobile_stations (mac) VALUES (%s)', [mac])
                    mobile_station_id = cur.lastrowid

                cur.execute('INSERT INTO probe_requests (ssid_id, mobile_station_id, ant_signal, last_seen_on) VALUES(%s, %s, %s, NOW())', [ssid_id, mobile_station_id, signaal])
                db.commit()
                sys.stdout.flush()
        else:
            break


def main():
  if not os.geteuid() == 0:
    sys.exit('Script moet uitgevoerd worden als root')
  prepareInterface()
  if kanaal_wisselen:
      randThread = RandomizeChannelThread()
      randThread.daemon = True
      randThread.start()
  startProbing()

if __name__ == "__main__":
    main()
