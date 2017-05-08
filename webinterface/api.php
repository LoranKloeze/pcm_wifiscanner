<?php
/*
 * PCM Wifiscanner
 * 
 * Copyright 2017 Loran Kloeze - loran@ralon.nl
 * Licentie: MIT
*/
switch (filter_input(INPUT_GET, 'act', FILTER_SANITIZE_STRING)) {
            case 'mobile_stations':
                $results = returnMobileStations();
                break;
            case 'ssids':
                $results = returnSsids();
                break;            
            case 'truncate_db':
                if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                   $results = truncateDb();
                } else {
                    die('Wrong method');
                }  
                break;
            default:
                die();
                break;
        }
        
header('Content-type:application/json;charset=utf-8');
echo json_encode($results); 

function returnMobileStations() {
    $conn = getDB();
    
    $sql = "SELECT probe_requests.mobile_station_id AS mobile_station_id, MAX(probe_requests.last_seen_on) AS max_last_seen_on, MAX(UNIX_TIMESTAMP(probe_requests.last_seen_on)) AS max_last_seen_on_ts, mobile_stations.mac FROM probe_requests INNER JOIN mobile_stations ON probe_requests.mobile_station_id = mobile_stations.id GROUP BY probe_requests.mobile_station_id ORDER BY max_last_seen_on ASC;";
    $result = $conn->query($sql);
    $rows = array();
    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    $conn->close();
    return $rows;
}

function returnSsids() {
    $conn = getDB();
    
    $sql = "SELECT probe_requests.mobile_station_id, mobile_stations.mac, ssids.ssid FROM probe_requests INNER JOIN ssids ON probe_requests.ssid_id = ssids.id INNER JOIN mobile_stations ON probe_requests.mobile_station_id = mobile_stations.id GROUP BY probe_requests.mobile_station_id, probe_requests.ssid_id ORDER BY mobile_stations.mac, ssids.ssid";
    $result = $conn->query($sql);
    $rows = array();
    while($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    $conn->close();
    return $rows;
}

function truncateDb() {
    $conn = getDB();    
    $sql = "TRUNCATE TABLE probe_requests; TRUNCATE TABLE ssids; TRUNCATE TABLE mobile_stations;";
    $conn->multi_query($sql);
    $conn->close();
    return true;
}

function getDB() {
    $servername = "localhost";
    $username = "wifiscan";
    $password = "wifiscan";
    $database = "wifiscanner";

    $conn = new mysqli($servername, $username, $password,$database);

    if ($conn->connect_error) {
        die("Verbinding met de database mislukt: " . $conn->connect_error);
    } 
    
    return $conn;
}