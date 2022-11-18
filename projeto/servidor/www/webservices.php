<?php
// ficheiro com as configuracoes todas necessarias
include 'config.php';

$macaddress = "";

// recolha dos parametros/atributos passados ao servico
if ($_GET) {
    //echo "valor passado pela url no endereco";
    $macaddress = $_GET['macaddress'];
    $ipaddress = $_GET['ipaddress'];
    $valled = $_GET['valled'];
    $stateled = $_GET['stateled'];
    $valldr = $_GET['valldr'];
    $valldrnew = $_GET['valldrnew'];
    $valpir = $_GET['valpir'];
    $statepir = $_GET['statepir'];

    if ( $macaddress =="")
        {
        //echo "valor passado como atributo";
        $macaddress = $attrs['macaddress'];
        $ipaddress = $attrs['ipaddress'];
        $valled = $attrs['valled'];
        $stateled = $attrs['stateled'];
        $valldr = $attrs['valldr'];
        $valldrnew = $attrs['valldrnew'];
        $valpir = $attrs['valpir'];
        $statepir = $attrs['statepir'];
        }
    }
    if ( $macaddress =="")
        {
        //echo "valores por defeito";
        $macaddress = '';
        $ipaddress = '';
        $valled = "";
        $stateled = "";
        $valldr = "";
        $valldrnew = "";
        $valpir = "";
        $statepir = "";
        }

echo "<h2>webservices.php</h2>";
echo "<br>macaddress ".$macaddress;
echo "<br>ipaddress ".$ipaddress;
echo "<br>valled ".$valled;
echo "<br>stateled ".$stateled;
echo "<br>valldr ". $valldr;
echo "<br>valldrnew ".$valldrnew;
echo "<br>valpir ".$valpir;
echo "<br>statepir ".$statepir;
echo "<br>";

if ( $macaddress !="") {
    // ligacao a base de dados
    $mysqli = new mysqli($bd_server,  $bd_user, $bd_passwd, $bd);
      
    // verifica a conetividade com a base de dados
    if ($mysqli === false) {
        die("ERROR: Could not connect. ".$mysqli->connect_error);
    } else {
        echo "<br>sql connection sucessfull<br>";
    }


    echo "<br>checking if macaddress ".$macaddress." exists...";

    $sql = "SELECT iddevices FROM devices WHERE macaddress = '".$macaddress."'";
    echo "<br>mysql: ".$sql;

    $result = $mysqli->query($sql);

    while ($valor = $result->fetch_array(MYSQLI_BOTH)){
      $iddevice = $valor["iddevices"];
    }

    echo "<br>";
    echo "<br>populating tables...";

        if (mysqli_num_rows($result)>0) { // caso existe
            mysqli_free_result($result);
            echo "<br>iddevice: ".$iddevice;
            echo "<br>";

            $sql = "INSERT INTO logs (ipaddress, valled, stateled, valldr, valldrnew, valpir, statepir, devices_iddevices)
                  VALUES('".$ipaddress."', ".$valled.", ".$stateled.", ". $valldr.", ".$valldrnew.", ".$valpir.", ".$statepir.", ".$iddevice.")";

            // executa o comando sql gerado anteriormente
            if ($mysqli->query($sql) === true) // sucesso na insercao
            {
                echo "<br>mysql: ".$sql;
                echo "<br>successfully inserted data!";
            }
        } else {            // caso nao existe
            mysqli_free_result($result);
            echo "<br>macaddress does not exist, let's create a record...";
            $sql = "INSERT INTO devices (macaddress, coordinatex, coordinatey)
                    VALUES('".$macaddress."', 0, 0)";
            // executa o comando sql gerado anteriormente
            if ($mysqli->query($sql) === true) // sucesso na insercao
            {
                echo "<br>mysql: ".$sql;
                echo "<br>successfully inserted macaddress!";
            }
        }
} else {
    echo "<br>nothing to do...";
}
?>