<?php

// Current date and time.
$date = new DateTime();
$current_time = $date->getTimestamp();

// Get values.
require 'vendor/autoload.php';

$realPower_text = $_GET['realPower'];
$apparentPower_text = $_GET['apparentPower'];
$Irms_text = $_GET['Irms'];

$realPower =  explode('p',$realPower_text);
$apparentPower =  explode('p',$apparentPower_text);
$Irms =  explode('p',$Irms_text);

$host = 'localhost';
$port = '8086';
$username = 'peepraeza';
$password = '029064755';
$client = new \InfluxDB\Client($host);

$database = $client->selectDB('Monitor');

$points[] = new \InfluxDB\Point('energy', 
								null, 
								['host' => 'server01'],
								['realPower1' => (float)$realPower[0], 
								 'realPower2' => (float)$realPower[1],
								 'realPower3' => (float)$realPower[2],
								 'realPower4' => (float)$realPower[3],
								 'apparentPower1' => (float)$apparentPower[0],
								 'apparentPower2' => (float)$apparentPower[1],
								 'apparentPower3' => (float)$apparentPower[2],
								 'apparentPower4' => (float)$apparentPower[3],
								 'Irms1' => (float)$Irms[0],
								 'Irms2' => (float)$Irms[1], 
								 'Irms3' => (float)$Irms[2], 
								 'Irms4' => (float)$Irms[3]],

								(int) $current_time
    							);
// print_r("BeforeDB");
$database->writePoints($points,\InfluxDB\Database::PRECISION_SECONDS);
print_r("Finished");
clearstatcache(); // clear cache after opload to database
?>