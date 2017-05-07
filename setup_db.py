#!/usr/bin/env python
import MySQLdb
import getpass
import pdb

# Instellingen
database_naam = 'wifiscanner'

mysql_wachtwoord = getpass.getpass("MySQL wachtwoord voor root@localhost: ")

db = MySQLdb.connect(host="localhost",    
                     user="root",       
                     passwd=mysql_wachtwoord)

cur = db.cursor()

# Database aanmaken
print "[+] Database " + database_naam + " aanmaken..."
cur.execute("CREATE DATABASE IF NOT EXISTS "  + database_naam)

# Database instellen als actieve database
cur.execute("USE " + database_naam)

# Tabel 'mobile_stations' aanmaken
print "[+] Tabel mobile_stations aanmaken..."
cur.execute("CREATE TABLE IF NOT EXISTS mobile_stations (id INT NOT NULL AUTO_INCREMENT, mac CHAR (17) NOT NULL UNIQUE, INDEX(mac(17)), PRIMARY KEY (id))")

# Tabel 'ssids' aanmaken 
print "[+] Tabel ssids aanmaken..."
cur.execute("CREATE TABLE IF NOT EXISTS ssids (id INT NOT NULL AUTO_INCREMENT, ssid CHAR (32) NOT NULL UNIQUE, INDEX(ssid(32)), PRIMARY KEY (id))")

# Tabel 'probe_requests' aanmaken
print "[+] Tabel probe_requests aanmaken..."
cur.execute("CREATE TABLE IF NOT EXISTS probe_requests (id INT NOT NULL AUTO_INCREMENT, ssid_id INT NOT NULL, mobile_station_id INT NOT NULL, ant_signal SMALLINT, last_seen_on TIMESTAMP NOT NULL, FOREIGN KEY (ssid_id) REFERENCES ssids(id), FOREIGN KEY (mobile_station_id) REFERENCES mobile_stations(id), PRIMARY KEY (id))")

# View 'view_requests' aanmaken
print "[+] View view_requests aanmaken..."
cur.execute("CREATE VIEW view_requests AS select probe_requests.id, probe_requests.last_seen_on, mobile_stations.mac, ssids.ssid, probe_requests.ant_signal from probe_requests INNER JOIN ssids ON probe_requests.ssid_id = ssids.id INNER JOIN mobile_stations ON probe_requests.mobile_station_id = mobile_stations.id ORDER BY probe_requests.last_seen_on;")

# Gebruiker 'wifiscan' aanmaken
print "[+] Gebruiker wifiscan aanmaken"
cur.execute("CREATE USER 'wifiscan'@'localhost' IDENTIFIED BY 'wifiscan'")
cur.execute("GRANT ALL PRIVILEGES ON " + database_naam + ".* TO 'wifiscan'@'localhost'")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[0]

db.close()
