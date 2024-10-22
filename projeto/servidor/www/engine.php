
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

//------------------------------------------------
if($_GET['method']=="select"){                                                            // method: select
//------------------------------------------------
  if($_GET['object']=="users"){                                                           // object: users
    $sql = "select * from users";
    if($_GET['idusers']!="") { 
      $sql = $sql . ' where idusers="'.$_GET["idusers"].'"';
    }
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
//------------------------------------------------
  if($_GET['object']=="devices"){                                                           // object: devices
    $sql = "select * from devices";
    if($_GET['iddevices']!="") { 
      $sql = $sql . ' where iddevices="'.$_GET["iddevices"].'"';
    }
    $result = $mysqli->query($sql);
    if($result->num_rows > 0){
      echo '{"status":"ok","totalResults":"'.$result->num_rows.'","'.$_GET['object'].'":[';
      for ($i=0;$i<mysqli_num_rows($result);$i++) {
        $res = ($i>0?',':'').json_encode(mysqli_fetch_object($result));
        echo substr($res, 0,-1);
        echo ",";

        // status: online / offline
        $value=strstr($res,':');
        $value=strstr($value,'datetime',true);
        $value=ltrim($value, ':"');
        $value=substr($value, 0,-3);
        $sql2 = 'select if(timediff(now(),logs.datetime)<"'.$onlineTime.'","online","offline") as status FROM smartenergy.devices left join logs on devices.iddevices=devices_iddevices where devices_iddevices = "'.$value.'" order by logs.datetime desc limit 1';
        //echo $sql2;
        $result2 = $mysqli->query($sql2);
        if (mysqli_num_rows($result2)==0) echo '"status":"offline"}';
        for ($j=0;$j<mysqli_num_rows($result2);$j++) {
          $res2 = ($j>0?',':'').json_encode(mysqli_fetch_object($result2));
          echo ltrim($res2, '{');
        }
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
  //------------------------------------------------
  if($_GET['object']=="logs"){                                                           // object: logs
    $sql = "select * from logs";
    if($_GET['devices_iddevices']!="") { 
      $sql = $sql . ' where devices_iddevices="'.$_GET["devices_iddevices"].'"';
    }
    $sql = $sql. ' order by datetime desc limit 100';
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
  //------------------------------------------------
  if($_GET['object']=="devicestatus"){                                                           // object: devicestatus, get a device and status
    if($_GET['devices_iddevices']!="") {
      $sql = 'select *, if(timediff(now(),datetime)<"'.$onlineTime.'","online","offline") as status from smartenergy.logs';
      $sql = $sql . ' where devices_iddevices="'.$_GET["devices_iddevices"].'"';
      $sql = $sql . ' order by idlogs desc limit 1';
     } else {
      $sql = "select * from (select * from smartenergy.logs";
      $sql = $sql. '  order by idlogs desc) as tmp_table group by devices_iddevices;';
     }

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

  //------------------------------------------------
  if($_GET['object']=="devicesstatus"){                                                           // object: devicesstatus, get all devices and status
    $sql = "select iddevices, macaddress, detail, coordinatex, coordinatey from devices";
    if($_GET['iddevices']!="") { 
      $sql = $sql . ' where iddevices="'.$_GET["iddevices"].'"';
    }
    $result = $mysqli->query($sql);
    if($result->num_rows > 0){
      echo '{"status":"ok","totalResults":"'.$result->num_rows.'","'.$_GET['object'].'":[';
      for ($i=0;$i<mysqli_num_rows($result);$i++) {
        $res = ($i>0?',':'').json_encode(mysqli_fetch_object($result));
        echo substr($res, 0,-1);
        echo ",";

        // status: online / offline
        $value=strstr($res,':');
        $value=strstr($value,'macaddress',true);
        $value=ltrim($value, ':"');
        $value=substr($value, 0,-3);
        $sql2 = 'select *, if(timediff(now(),datetime)<"'.$onlineTime.'","online","offline") as status from smartenergy.logs';
        $sql2 = $sql2 . ' where devices_iddevices="'.$value.'"';
        $sql2 = $sql2 . ' order by idlogs desc limit 1';
        //echo $sql2;
        $result2 = $mysqli->query($sql2);
        if (mysqli_num_rows($result2)==0) echo '"status":"offline"}';
        for ($j=0;$j<mysqli_num_rows($result2);$j++) {
          $res2 = ($j>0?',':'').json_encode(mysqli_fetch_object($result2));
          echo ltrim($res2, '{');
        }
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
?>