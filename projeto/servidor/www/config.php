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

flush();
// Configurações gerais
$pasta="/var/www/html/";   // localizacao do site;

// Configuração do servidor mysql
$bd_server = "localhost";       // Nome ou IP do servidor
$bd ="smartenergy";              // Nome da Base de Dados

// mysql read & write perms
$bd_user = "se";                 // Username
$bd_passwd = "smartenergy";      // Palavra Passe

// tempos
$onlineTime = "00:05:00";		// tempo para considerar um poste de iluminacao online (HH:MM:SS)
?>

