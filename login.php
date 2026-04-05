<?php session_start(); ?>

<!DOCTYPE html>
<html>

<head>
	<title>php test</title>

</head>

<body>
	<form action="" method="post">
		<label for="username">Username: </label>
		<input type="text" name="username"> <br>
		<label for="password">Password: </label>
		<input type="password" name="password"> <br>
		<button type="submit" name="login">Login</button> <br>
	</form>

</body>

</html>

<?php

try {$conn = mysqli_connect("localhost" , "root" , "" , "login");}
catch (mysqli_sql_exception) {echo "connection error";}




if (isset($_POST['login'])) {
	$username = trim($_POST['username'] ?? "");
	$password = trim($_POST['password'] ?? "");
	
	$sql = "SELECT * FROM login WHERE username='$username'";
	$result = $conn->query($sql);

	if ($result->num_rows === 1) {
		$user = $result->fetch_assoc();

		if (password_verify($password, $user['password'])) {
			$_SESSION['username'] = $user['username'];
			$_SESSION['logged-in'] = true;
			header("Location: dashboard.php");
		} else {
			echo "Wrong password";
		}
	} else {
		echo "User not found";
	}
}

?>