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

if($_GET['method']=="login"){
		$username= $_GET["username"];
	    $password= $_GET["password"];

		// ligacao a base de dados
		$mysqli = new mysqli($bd_server,  $bd_user, $bd_passwd, $bd);
	
		// verifica a conetividade com a base de dados
		if ($mysqli === false) {
			die("ERROR: Could not connect. ".$mysqli->connect_error);
		} else {
			//echo "<br>sql connection sucessfull<br>";
		}
		
		// query a base de dados se existe o username com a password
    	$sql = "select * from users where username='$username' and password='$password'";
		$result = $mysqli->query($sql);
		
		if($result->num_rows > 0){
			// inicializa valores de nao acesso / login invalido
			$output['response'] = "false";
			$output['userid'] = "no_record_found";
			$output['name'] = "no_record_found";
			$output['username'] = "no_record_found";

			// coloca os valores corretos do login, username, name
			$row = $result->fetch_assoc();
			$output["response"] = trim("true");
			$output["userid"] = trim($row["idusers"]);
			$name = str_replace(" ","_",$row['name']);
			$output["name"] = trim($name);
			$username = str_replace(" ","_",$row['username']);
			$output["username"] = trim($username);
		}else{
			$output['response'] = "false";
			$output['userid'] = "no_record_found";
			$output['name'] = "no_record_found";
			$output['username'] = "no_record_found";
		}
	echo json_encode($output);
	}