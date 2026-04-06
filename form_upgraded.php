<?php
if(isset($_POST['login']))
	{header("Location: login.php");
	exit();}
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
		<label for="email"> Email: </label>
		<input name="email" id="email" type="text"> <br>
		<label for="password">Password: </label>
		<input type="password" name="password"> <br>
		<label for="username">Username: </label>
		<input type="text" name="username"> <br>
		<button type="submit">Register</button> <br>
		<button type="submit" name="login">Login</button> <br>
	</form>

</body>

</html>

<?php

$db_server = "localhost";
$db_user = "root";
$db_password = "";
$db_name = "login";
$conn = "";

try {$conn = mysqli_connect($db_server , $db_user , $db_password , $db_name);}
catch (mysqli_sql_exception) {echo "connection error";}


if($conn) 
    {echo nl2br("you are connected\n");}


$name = trim($_POST['name']);
$email = trim($_POST['email']);
$age = trim($_POST['age']);
$password = trim($_POST['password']);
$username = trim($_POST['username']);
$hashed = password_hash($password , PASSWORD_DEFAULT);

$errors = [];

if (!preg_match("/^[A-Za-z\s]+$/" , $name)) 
	{$errors[] = "only use letters";}

if (!filter_var ($email , FILTER_VALIDATE_EMAIL)) 
	{$errors[] = "invalid email";}

if (!preg_match("/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/", $password))
	{$errors[] = "doesnt meet password requirements";}

if(strlen($username) >= 15)
	{$errors[] = "username should be max. 15 characters";}

if (empty($errors)) 
	{echo nl2br("there was no error\n");
	echo nl2br("you are succesfully registered\n");

	$prepared = $conn->prepare("INSERT INTO login (name, mail, age, password, username) VALUES (?, ?, ?, ?, ?)");
	$prepared->bind_param("ssiss", $username, $email, $age, $hashed, $username);
	$prepared->execute();}
	
	if ($conn->connect_error) {
 	   die("Connection failed");
}
else {foreach($errors as $error){
	echo nl2br("$error\n");
}} 

$result = $conn->query("SELECT * FROM login");

echo "<h3>Registered Users:</h3>";

while ($row = $result->fetch_assoc()) {
    echo "<div>";
    echo "Username: " . htmlspecialchars($row["username"]) . "<br>";
    echo "</div><hr>";
}

echo "this is the user:" . $_SESSION['username']; //test to see if the session is destroyed or not

?>