<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link rel="stylesheet" href="../css/style_login.css">
</head>
<body>
    <div class="caja_principal">
        <div class="caja_trasera">
            <div class="caja_trasera-login">
                <h1>¿Ya tienes cuenta?</h1>
                <p>Inicia sesión para entrar en la pagina</p>
                <button id="btn_Iniciar-Sesión">Iniciar Sesión</button>

            </div>
            <div class="caja_trasera-register">
                <h1>¿Aún no tienes una cuenta?</h1>
                <p>Regístrate para iniciar sesión</p>
                <button id="btn_registrarse">Regístrarse</button>
            </div>
        </div>
        <div class="contenedor_login-register">
            <form action="../php/inicio_sesion.php" method = "POST"  class="formulario_login">
                <h2>Iniciar Sesión</h2>
                <input type="text" placeholder="User" name = "User">
                <input type="password" placeholder="Password" name = "password">
                <button>Ingresar</button>
            </form>
            <form action="../php/registro_usuario.php" method = "POST" class="formulario_register">
                <h2>Regístrarse</h2>
                <input type="text" placeholder="Nombre Completo" name = "nombre_completo">
                <input type="text" placeholder="Correo Electronico" name = "correo">
                <input type="text" placeholder="User" name = "user">
                <input type="password" placeholder="Password" name = "password">
                <button>Regístrarse</button>
            </form>
        </div>
    </div>
	<script src="../js/script.js"></script>
</body>
</html>