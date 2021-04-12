<?php

/* Conexión con la base de datos, se debe especificar en donde se encuentra la base de datos, el nombre de la base de datos,
la clave de la base de datos y el nombre de la tabla en la que vamos a ingresar*/

$conexion = mysqli_connect("fdb27.125mb.com", "3797781_usuarios", "Base0627", "3797781_usuarios");

/* Codigo para confirmar que se realizó la conexión de forma correcta*/

/*
if($conexion){
    echo 'Conexión exitosa a base de datos';
}else{
    echo 'Error en la conexión a base de datos';
}

*/

?>