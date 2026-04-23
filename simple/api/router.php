<?php
require '../vendor/autoload.php';
require 'response.php';
require 'db.php';
require 'middleware.php';
require 'tasks.php';

header("Content-Type: application/json");
$data = json_decode(file_get_contents("php://input"), true);
$method = $_SERVER['REQUEST_METHOD'];
$user_id = authenticate();
$id = $data['task_id'] ?? null;

switch ($method) {
    case "GET":
        viewTask($conn, $user_id);
        break;

    case "POST":
        createTask($conn,$user_id,$data);
        break;

    case "DELETE":
        deleteTask($conn, $id,$user_id);
        break;

    case "PUT":
        completeTask($conn, $id,$user_id);
        break;

    default:
        sendResponse("error", "Method not allowed", null, 405);
}
?>