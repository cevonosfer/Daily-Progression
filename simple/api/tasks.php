<?php

function createTask($conn,$user_id,$data){
$task = $data['task'];

$stmt = $conn->prepare("INSERT INTO tasks (name, user_id) VALUES (?, ?)");
$stmt->bind_param("si", $task, $user_id);

if ($stmt->execute()) {
    sendResponse("success" , "task added" , null , 201);
}
}

function viewTask($conn,$user_id){
$stmt = $conn->prepare("SELECT * FROM tasks WHERE user_id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$tasks = [];

while ($row = $result->fetch_assoc()) {
    $tasks[] = $row;
}
echo json_encode($tasks);
}

function deleteTask($conn,$id,$user_id){

$stmt = $conn->prepare("DELETE FROM tasks WHERE id = ? AND user_id = ?");
$stmt->bind_param("ii", $id,$user_id);

if ($stmt->execute()) {
    sendResponse("success" , "task deleted" , null , 201);
}
}

function completeTask($conn,$id,$user_id){

$stmt = $conn->prepare("UPDATE tasks SET is_done='done' WHERE id = ? AND user_id = ?");
$stmt->bind_param("ii", $id,$user_id);

if ($stmt->execute()) {
    sendResponse("success" , "task completed" , null , 201);
}
}
?>