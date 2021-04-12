<?php

include 'conexion.php'; // Se llama al archivo de conexion para realizar la conexión con la base de datos

// Se crean las variables utilizadas para hacer el registro de los nuevos usuarios, la transmisión es tipo POST

$nombre_completo = $_POST['nombre_completo'];
$correo = $_POST['correo'];
$user = $_POST['user'];
$password = $_POST['password'];

//Encriptar contraseña con algoritmo sha512

$password = hash('sha512', $password); 

//Se especifican los datos que se almacenaran en la base de datos, deben estar en orden  

$query = "INSERT INTO usuarios(nombre_completo, correo, user, password)
          VALUES('$nombre_completo' , '$correo', '$user', '$password')";

//Verificación de no repetición de usuario ni correo

$verificacion_correo = mysqli_query($conexion, "SELECT * FROM usuarios WHERE correo = '$correo'");

if(mysqli_num_rows($verificacion_correo) > 0){ // Se realiza la comparación entre los datos ingresados y los existentes en la base de datos
    echo'
        <script>
            alert("Este correo electronico ya está registrado, intenta con otro");
            window.location = "../login/index.php";
            </script>
    
    ';
    exit();
}

$ejecutar = mysqli_query($conexion, $query); // Se realiza la tranferencia de los datos a la base de datos

if($ejecutar){   // Se imprime un mensaje de registro exitoso si el almacenamento de los datos fue correcto y se devuelve al login para el inicio de sesión
    echo '
        <script>
            alert("Regístro exitoso");
            window.location = "../login/index.php";
        </script>
    
    ';
}else{ // En caso de existir algun error se imprime un mensaje de error y se devulve al login para interntar el registro de nuevo
    echo '
        <script>
            alert("Regístro fallido, intentalo de nuevo");
            window.location = "../login/index.php";
        </script>
    ';    
}

mysqli_close($conexion) // Se cierra la conexión con la base de datos para evitar posibles inconvenientes 
?>