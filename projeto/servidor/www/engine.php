
<?php
/*
  Project: Smart Energy Campus
  Year   : 2022 / 2023
           LESI @ IPCA
  Authors:  2727 Nuno Mendes
           21138 Rosario Silva
           21153 Tiago Azevedo
           21156 Francisco Pereira
*/

date_default_timezone_set("Europe/Lisbon");
include 'config.php';
$output = array();
$input = array();
$response = array();

// ligacao a base de dados
$mysqli = new mysqli($bd_server,  $bd_user, $bd_passwd, $bd);
// verifica a conetividade com a base de dados
if ($mysqli === false) {
  die("ERROR: Could not connect. ".$mysqli->connect_error);
} else {
  //echo "<br>sql connection sucessfull<br>";
}

if($_GET['method']=="select"){
  if($_GET['object']=="users"){
    
    // query a base de dados se existe o username com a password
    $sql = "select * from users";
    $result = $mysqli->query($sql);
    
    if($result->num_rows > 0){
      echo '{"status":"ok","totalResults":"'.$result->num_rows.'","'.$_GET['object'].'":[';
      for ($i=0;$i<mysqli_num_rows($result);$i++) {
        echo ($i>0?',':'').json_encode(mysqli_fetch_object($result));
      }
      echo ']}';

    }else{
      $output['response'] = "false";
      $output['userid'] = "no_record_found";
      $output['name'] = "no_record_found";
      $output['username'] = "no_record_found";
      $output['password'] = "no_record_found";
      $output['permission'] = "no_record_found";
      echo json_encode($output);
    }
  }

  if($_GET['object']=="devices"){
    
    // query a base de dados se existe o username com a password
    $sql = "select * from devices";
    $result = $mysqli->query($sql);
    
    if($result->num_rows > 0){
      echo '{"status":"ok","totalResults":"'.$result->num_rows.'","'.$_GET['object'].'":[';
      for ($i=0;$i<mysqli_num_rows($result);$i++) {
        echo ($i>0?',':'').json_encode(mysqli_fetch_object($result));
      }
      echo ']}';

    }else{
      $output['response'] = "false";
      $output['iddevices'] = "no_record_found";
      $output['macaddress'] = "no_record_found";
      $output['coordinatex'] = "no_record_found";
      $output['coordinatey'] = "no_record_found";
      echo json_encode($output);
    }
  }
}