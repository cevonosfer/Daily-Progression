<?php 
require "api\db.php";
require 'api\response.php';
$data = json_decode(file_get_contents("php://input"), true);

function register($conn,$data){

$name = trim($data['name'] ?? '');
$email = trim($data['mail'] ?? '');
$age = $data['age'] ?? null;
$username = trim($data['username'] ?? '');
$password = $data['password'] ?? '';
$hashed = password_hash($password, PASSWORD_DEFAULT);

if (!$name || !$email || !$age || !$username || !$password) {
    sendResponse("error", "All fields are required", null, 400);
}

if (!preg_match("/^[A-Za-z\s]+$/", $name)) {
    sendResponse("error", "Name must contain only letters", null, 400);
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    sendResponse("error", "Invalid email format", null, 400);
}

if (strlen($username) > 15) {
    sendResponse("error", "Username max length is 15", null, 400);
}

if (!preg_match("/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/", $password)) {
    sendResponse("error", "Weak password", null, 400);
}

$stmt = $conn->prepare("SELECT id FROM users WHERE username = ? OR mail = ?");
$stmt->bind_param("ss", $username, $email);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    sendResponse("error", "Username or email already exists", null, 409);
}

$stmt = $conn->prepare("
    INSERT INTO users (name, mail, age, username, password)
    VALUES (?, ?, ?, ?, ?)
");

$stmt->bind_param("ssiss", $name, $email, $age, $username, $hashed);

if (!$stmt->execute()) {
    sendResponse("error", "Database error while creating user", null, 500);
}

sendResponse("success", "User registered successfully", [
    "username" => $username,
    "email" => $email
], 201);
}

function login($conn,$data){

$username = $data['username'];
$password = $data['password'];

$stmt = $conn->prepare("SELECT * FROM users WHERE username = ?");
$stmt->bind_param("s", $username);
$stmt->execute();

$result = $stmt->get_result();

if ($result->num_rows === 1) {
    $user = $result->fetch_assoc();

    if (password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['user_id'];
        $_SESSION['username'] = $user['username'];

        echo json_encode([
            "message" => "Login successful",
            "user_id" => $user['user_id']
        ]);
    } else {
        sendResponse("error" , "invalid password or email" , null , 400);
    }
} else {
    sendResponse("error" , "user not found" , null , 400);
}
}
?>
