<?php
require 'api\db.php';
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function authenticate() {
    $headers = getallheaders();
    $authHeader = $headers['Authorization'] ?? '';

    if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
        sendResponse("error", "Unauthorized", null, 401);
    }

    $token = substr($authHeader, 7); // remove "Bearer "

    try {
        $decoded = JWT::decode($token, new Key(JWT_SECRET, 'HS256'));
        return $decoded->user_id;
    } catch (Exception $e) {
        sendResponse("error", "Invalid or expired token", null, 401);
    }
}
?>