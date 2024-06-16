<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creación de Usuario</title>
</head>
<?php
    // Inicia una nueva sesión o reanuda la existente
    session_start();

    // Se inicia el CURL
    $ch = curl_init();

    // URL del endpoint
    $url = "http://localhost:8000/aficionado/";

    // Se crea un array con los datos del usuario
    $data = array(
        "id_aficionado" => "1",
        "username" => "luis_garcia",
        "password" => "1234",
        "gmail" => "luis.garcia@example.com",
        "birthdate" => "1990-05-15",
        "registerdate" => "1991-05-15",
        "id_equipo" => "1",
        "url_avatar" => "https://cdn-icons-png.flaticon.com/512/4792/4792929.png"
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
    if(curl_errno($ch)){
        $error_msg = 'Error de curl: ' . curl_error($ch); //Error de petición
    }elseif ($response === false){
        $error_msg = 'Error en la respuesta. Respuesta vacía';
    }else{
        // Decodifica la respuesta convirtiendo el JSON en un array
        $response_data = json_decode($response, true);
        if (isset($response_data['error'])) {
            $error_msg = 'Error: ' . $response_data['error'];
        } else {
            $success_msg = 'Usuario registrado exitosamente';
        }
    }

    // Cierra el CURL
    curl_close($ch);
?>
<body>
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