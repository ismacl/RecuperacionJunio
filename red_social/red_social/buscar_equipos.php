<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscar Equipos</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 15px;
            text-align: left;
        }
        img {
            width: 100px;
            height: auto;
        }
    </style>
</head>
<body>
    <h2>Buscar Equipos</h2>
    <!-- Formulario para buscar equipos -->
    <form action="buscar_equipos.php" method="get">
        <label for="equipo">Equipo:</label>
        <input type="text" id="equipo" name="equipo"><br><br>

        <label for="liga">Liga:</label>
        <input type="text" id="liga" name="liga"><br><br>

        <label for="pais">País:</label>
        <input type="text" id="pais" name="pais"><br><br>

        <label for="año_fundacion">Año de Fundación:</label>
        <input type="number" id="año_fundacion" name="año_fundacion"><br><br>

        <label for="estadio">Estadio:</label>
        <input type="text" id="estadio" name="estadio"><br><br>

        <label for="url_equipo">URL del Equipo:</label>
        <input type="text" id="url_equipo" name="url_equipo"><br><br>

        <button type="submit">Buscar</button>
    </form>

    <?php
    // Recuperamos los valores del formulario
    $equipo = $_GET['equipo'] ?? '';
    $liga = $_GET['liga'] ?? '';
    $pais = $_GET['pais'] ?? '';
    $año_fundacion = $_GET['año_fundacion'] ?? '';
    $estadio = $_GET['estadio'] ?? '';
    $url_equipo = $_GET['url_equipo'] ?? '';

    // Verificamos si se ha indicado al menos un criterio de búsqueda
    if (empty($equipo) && empty($liga) && empty($pais) && empty($año_fundacion) && empty($estadio) && empty($url_equipo)) {
        echo '<p>No se ha indicado ningún criterio de búsqueda.</p>';
    } else {
        // Inicializamos una nueva solicitud cURL
        $ch = curl_init();

        // URL para la búsqueda de equipos en Django
        $baseUrl = "http://localhost:8000/equipos/search";

        // Construimos los parámetros de la consulta con la función http_build_query
        $queryParams = http_build_query(array(
            'equipo' => $equipo,
            'liga' => $liga,
            'pais' => $pais,
            'año_fundacion' => $año_fundacion,
            'estadio' => $estadio,
            'url_equipo' => $url_equipo
        ));

        // Construimos la URL completa con los parámetros de la consulta
        $url = $baseUrl . '?' . $queryParams;

        // Establecemos la URL de la solicitud cURL
        curl_setopt($ch, CURLOPT_URL, $url);

        // Configuramos cURL para devolver el resultado como una cadena en lugar de imprimirlo directamente
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        // Ejecutamos la solicitud cURL y almacenamos la respuesta
        $response = curl_exec($ch);

        // Manejamos errores de cURL
        if (curl_errno($ch)) {
            echo 'Error de cURL: ' . curl_error($ch);
        } elseif ($response === false) {
            echo 'Error en la respuesta. Respuesta vacía';
        } else {
            // Obtenemos el código de estado HTTP de la respuesta
            $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

            // Si el código de estado es 200 (OK), procesamos la respuesta
            if ($http_code == 200) {
                // Decodificamos la respuesta JSON en un array 
                $response_data = json_decode($response, true);

                // Verificamos si la respuesta no está vacía
                if (!empty($response_data)) {
                    // Mostramos los resultados de la búsqueda en una tabla
                    echo '<h2>Resultados de la búsqueda:</h2>';
                    echo '<table>';
                    echo '<tr><th>Equipo</th><th>Liga</th><th>País</th><th>Año de Fundación</th><th>Estadio</th><th>URL del Equipo</th></tr>';

                    // Iteramos sobre cada equipo en la respuesta y lo mostramos en la tabla
                    foreach ($response_data as $equipo) {
                        echo '<tr>';
                        echo '<td>' . htmlspecialchars($equipo['equipo']) . '</td>';
                        echo '<td>' . htmlspecialchars($equipo['liga']) . '</td>';
                        echo '<td>' . htmlspecialchars($equipo['pais']) . '</td>';
                        echo '<td>' . htmlspecialchars($equipo['año_fundacion']) . '</td>';
                        echo '<td>' . htmlspecialchars($equipo['estadio']) . '</td>';
                        echo '<td><a href="' . htmlspecialchars($equipo['url_equipo']) . '">' . htmlspecialchars($equipo['url_equipo']) . '</a></td>';
                        echo '</tr>';
                    }

                    echo '</table>';
                } else {
                    // Si no se encontraron equipos, mostramos un mensaje de advertencia
                    echo '<p>No se encontraron equipos.</p>';
                }
            } else {
                // Si recibimos un código de estado HTTP diferente a 200, mostramos un mensaje de error
                echo "<p>Error HTTP: $http_code. No se pudo completar la búsqueda.</p>";
            }
        }

        // Cerramos la sesión cURL
        curl_close($ch);
    }
    ?>
</body>
</html>
