<?php
session_start();
require 'config.php';
if(isset($_POST['login']))
	{header("Location: login.php");
	exit();}

if ($_SERVER['REQUEST_METHOD'] == 'POST')
	{header("Location: " . $_SERVER['PHP_SELF']);
	exit();
	}
?>
<!DOCTYPE html>
<html>
<head>
	<title>php test</title>
</head>

<body>
	<form action="" method="POST">
		<label for="name">Name: </label>
		<input name="name" id="name" type="text" > <br>
		<label for="age">Age: </label>
		<input name="age" id="age" type="number"> <br>
		<label for="mail"> mail: </label>
		<input name="mail" id="mail" type="text"> <br>
		<label for="password">Password: </label>
		<input type="password" name="password"> <br>
		<label for="username">Username: </label>
		<input type="text" name="username"> <br>
		<button type="submit" name="register">Register</button> <br>
		<button type="submit" name="login">Login</button> <br>
	</form>
</body>
</html>

<?php
$name = trim($_POST['name']);
$mail = trim($_POST['mail']);
$age = trim($_POST['age']);
$password = trim($_POST['password']);
$username = trim($_POST['username']);
$hashed = password_hash($password , PASSWORD_DEFAULT);

$errors = [];
if(empty($name) || empty($mail) || empty($age) || empty($password) || empty($username))
	{$errors[] = "Please fill all the sections!";}

if (!preg_match("/^[A-Za-z\s]+$/" , $name)) 
	{$errors[] = "only use letters";}

if (!filter_var ($mail , FILTER_VALIDATE_EMAIL)) 
	{$errors[] = "invalid mail";}

if (!preg_match("/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/", $password))
	{$errors[] = "doesnt meet password requirements";}

if(strlen($username) >= 15)
	{$errors[] = "username should be max. 15 characters";}

if ($_POST['register'] && empty($errors)) 
	{echo nl2br("there was no error\n");
	echo nl2br("you are succesfully registered\n");

	$prepared = $conn->prepare("INSERT INTO users (name, mail, age, password, username) VALUES (?, ?, ?, ?, ?)");
	$prepared->bind_param("ssiss", $name, $mail, $age, $hashed, $username);
	$prepared->execute();}
	
	if ($conn->connect_error) {
 	   die("Connection failed");
}
else {foreach($errors as $error){
	echo nl2br("$error\n");
}} 

echo "this is the user:" . $_SESSION['username']; //test to see if the session is destroyed or not
?>