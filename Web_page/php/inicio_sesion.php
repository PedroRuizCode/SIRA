<?php

session_start();

include 'conexion.php';

$user = $_POST['User'];
$password = $_POST['password'];
$password = hash('sha512', $password);

$validacion_ingreso = mysqli_query($conexion, "SELECT * FROM usuarios WHERE User = '$user' and password = '$password' ");

if(mysqli_num_rows($validacion_ingreso) > 0){
    $_SESSION['user'] = $user;
   header("location:principal.php");
    exit();
}else{
    echo'
        <script>
            alert("Usuario no valido");
            window.location = "../login/index.php";
        </script>

    ';
    exit();
}
?>