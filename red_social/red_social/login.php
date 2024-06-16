<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Usuario</title>
</head>
<?php
    // Inicia una nueva sesión
    session_start();

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        // Se inicia el CURL
        $ch = curl_init();

        // URL del endpoint de login
        $url = "http://localhost:8000/session/";

        // Se crea un array
        $data = array(
            "username" => $_POST['username'],
            "password" => $_POST['password']
        );

        // Configuración de la solicitud POST
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); 
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        // Se ejecuta el CURL y se almacena la respuesta
        $response = curl_exec($ch);

        // Se capturan los errores de curl
        if (curl_errno($ch)) {
            $error_msg = 'Error de curl: ' . curl_error($ch); // Error de petición
        } elseif ($response === false) {
            $error_msg = 'Error en la respuesta. Respuesta vacía';
        } else {
            // Decodifica la respuesta convirtiendo el JSON en un array
            $response_data = json_decode($response, true);
            if (isset($response_data['error'])) {
                $error_msg = 'Error: ' . $response_data['error'];
            } else {
                $success_msg = 'Inicio de sesión exitoso';
                $_SESSION['token'] = $response_data['token']; // Guarda el token en la sesión
            }
        }

        // Cierra el CURL
        curl_close($ch);
    }
?>
<body>
    <!--Renderiza el formulario de login-->
    <h1>Inicio de Sesión</h1>
    <form method="post" action="">
        <label for="username">Nombre de usuario:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required><br><br>

        <button type="submit" name="login">Iniciar Sesión</button>
    </form>
    <!--Renderiza la respuesta-->
    <div class="message">
        <?php
            if (isset($error_msg)) {
                echo '<h1>' . $error_msg . '</h1>';
            } elseif (isset($success_msg)) {
                echo '<h1>' . $success_msg . '</h1>';
            }
        ?>
    </div>
</body>
</html>