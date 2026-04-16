<?php
require 'api\db.php';
require 'api\response.php';
header("Content-Type: application/json");

if (!isset($_SESSION['user_id'])) {
    sendResponse("error", "Unauthorized", null, 401);
}

$method = $_SERVER['REQUEST_METHOD'];
$data = json_decode(file_get_contents("php://input"), true);
$user_id = $_SESSION['user_id'];
$id = $data['task_id'];
require 'api\router.php';

function createTask($conn,$data,$user_id){
$task = $data['task'];

$stmt = $conn->prepare("INSERT INTO tasks (name, user_id) VALUES (?, ?)");
$stmt->bind_param("si", $task, $user_id);

if ($stmt->execute()) {
    sendResponse("success" , "task added" , null , 201);
}
}

function viewTask($conn,$user_id){
$result = $conn->query("SELECT * FROM tasks WHERE user_id = $user_id");
$tasks = [];

while ($row = $result->fetch_assoc()) {
    $tasks[] = $row;
}
echo json_encode($tasks);
}

function deleteTask($conn,$id){

$stmt = $conn->prepare("DELETE FROM tasks WHERE id = ?");
$stmt->bind_param("i", $id);

if ($stmt->execute()) {
    sendResponse("success" , "task deleted" , null , 201);
}
}

function completeTask($conn,$id){

$stmt = $conn->prepare("UPDATE tasks SET is_done='done' WHERE id = ?");
$stmt->bind_param("s", $id);

if ($stmt->execute()) {
    sendResponse("success" , "task completed" , null , 201);
}
}
?>