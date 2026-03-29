<!DOCTYPE html>
<html>

<head>
	<title>php test</title>

</head>

<body>
	<form action="index.php" method="post">
		<label for="name">Your name:</label>
		<input name="name" id="name" type="text" > <br>

		<label for="age">Your age:</label>
		<input name="age" id="age" type="number"> <br>
		<label for="email"> Email: </label>
		<input name="email" id="email" type="text"> <br>
		<button type="submit">Submit</button> <br>
	</form>

</body>

</html>

<?php

$db_server = "localhost";
$db_user = "root";
$db_password = "";
$db_name = "phpdb";
$conn = "";

try {$conn = mysqli_connect($db_server , $db_user , $db_password , $db_name);}
catch (mysqli_sql_exception) {echo "connection error";}


if($conn) 
    echo nl2br("you are connected\n");


$name = trim($_POST['name']);
$email = trim($_POST['email']);
$age = trim($_POST['age']);

$errors = [];

if (!preg_match("/^[A-Za-z\s]+$/" , $name)) 
	{$errors[] = "only use letters";}

if (!filter_vaR ($email , FILTER_VALIDATE_EMAIL)) 
	{$errors[] = "invalid email";}

if (empty($errors)) 
	{echo nl2br("there was no error\n");}
	$conn->query(
    "INSERT INTO users (name, email, age) 
     VALUES ('$name', '$email', $age)"
);
	if ($conn->connect_error) {
 	   die("Connection failed");
}
else {foreach($errors as $error){
	echo nl2br("$error\n");
}} 

$result = $conn->query("SELECT * FROM users");

echo "<h3>Registered Users:</h3>";

while ($row = $result->fetch_assoc()) {
    echo "<div>";
    echo "Name: " . htmlspecialchars($row["name"]) . "<br>";
    echo "Email: " . htmlspecialchars($row["email"]) . "<br>";
    echo "Age: " . htmlspecialchars($row["age"]);
    echo "</div><hr>";
}

?>