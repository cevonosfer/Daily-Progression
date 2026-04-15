<?php
require 'api\response.php';

$conn = new mysqli("localhost", "root", "", "login");

if ($conn->connect_error) {
    die(sendResponse("error" , "failed to connect to database" , null , 400));
}
?>