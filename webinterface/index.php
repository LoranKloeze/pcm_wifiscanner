<?php 
/*
 * PCM Wifiscanner
 * 
 * Copyright 2017 Loran Kloeze - loran@ralon.nl
 * Licentie: MIT
*/
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PCM Wifiscanner</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/app.css" rel="stylesheet">
  </head>
  <body>
      <div class="container">          
        <h1>PCM Wifiscanner</h1>
        <p>De onderstaande tabel laat mobile stations zien zoals telefoons/laptops/tablets e.d. die de afgelopen tijd zijn gevonden in de nabijheid van de Raspberry Pi. Elke regel toont het mac-adres van het mobile station met daarachter de access points waar het mobile station recentelijk verbinding mee heeft gehad. </p>
        <hr/>
        <div class='btn-group-xs'>
            <button id='btn-truncate-db' class='btn btn-xs btn-danger'>Database leeghalen</button>
            <button id='btn-pause' class='btn btn-xs btn-primary'>Updaten pauzeren</button>
        </div>
        <hr/>
        <table id='mobile_stations' class="table table-xs">
            <thead>
                <tr>
                    <th>MAC</th>
                    <th>SSID's</th>
                    <th>Laatst gezien</th>
                </tr>
            </thead>
            <tbody>
                
            </tbody>
        </table>
      </div>
      
    <script src="js/jquery-3.2.1.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/app.js"></script>
  </body>
</html>