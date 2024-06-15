<?php
session_start();

function registerAficionado($data) {
    $url = 'http://localhost:8000/crear_aficionado/';
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    
    $response = curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo 'Error de cURL: ' . curl_error($ch);
    } elseif ($response === false) {
        echo 'Error en la respuesta: La respuesta está vacía';
    } else {
        return json_decode($response, true);
    }
    
    curl_close($ch);
    return null;
}

$dataRegister = array(
    'id_aficionado' => '123',
    'username' => 'aficionado123',
    'password' => 'password123',
    'email' => 'aficionado123@example.com',
    'birthdate' => '2000-01-01',
    'url_avatar' => 'http://example.com/avatar.jpg'
);
$responseRegister = registerAficionado($dataRegister);
print_r($responseRegister);
?>

<h1>Registro de Aficionado</h1>
    <form method="post" action="">
        <label for="username">Nombre de usuario:</label>
        <input type="text" id="username" name="username" required><br><br>

        <label for="password">Contraseña:</label>
        <input type="password" id="password" name="password" required><br><br>

        <label for="email">Correo electrónico:</label>
        <input type="email" id="email" name="email" required><br><br>

        <label for="birthdate">Fecha de nacimiento:</label>
        <input type="date" id="birthdate" name="birthdate" required><br><br>

        <label for="avatar">URL del avatar:</label>
        <input type="url" id="avatar" name="avatar"><br><br>

        <button type="submit" name="register">Registrar</button>
    </form>