<!DOCTYPE html>
<html>
<head>

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

$name = trim($_POST['name']);
$email = trim($_POST['email']);
$age = trim($_POST['age']);

echo ("hello $name, your email is : $email and your age is : $age")

?>