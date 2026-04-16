<?php
require 'api\tasks.php';
require 'api\response.php';
$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case "GET":
        viewTask($conn, $user_id);
        break;

    case "POST":
        createTask($conn,$user_id,$data);
        break;

    case "DELETE":
        deleteTask($conn, $user_id);
        break;

    case "PUT":
        completeTask($conn, $user_id);
        break;

    default:
        sendResponse("error", "Method not allowed", null, 405);
}
?>