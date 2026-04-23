<?php
require '../api/response.php';

$conn = new mysqli("localhost", "root", "", "login");

if ($conn->connect_error) {
    die(sendResponse("error" , "failed to connect to database" , null , 400));
}
if (!defined('JWT_SECRET')) {
    define('JWT_SECRET', 'mY$uper$ecretKey!2024#TaskFlow@Secure123456');
}

if (!defined('JWT_EXPIRY')) {
    define('JWT_EXPIRY', 1800);
}
?>