<?php session_start(); ?>

<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        
        <form action="" method="POST">
        <button name="add">Add Task</button>
        <button name="add">View Tasks</button>
        <button name="logout">Log Out</button>
        </form>
    </body>
</html>


<?php

$db_server = "localhost";
$db_user = "root";
$db_password = "";
$db_name = "login";
$conn = "";
$is_completed = $conn -> query("SELECT is_done FROM tasks")

try {$conn = mysqli_connect($db_server , $db_user , $db_password , $db_name);}
catch (mysqli_sql_exception) {echo "connection error";}


echo "welcome" . $_SESSION['username'];

if (isset($_POST['delete'])) 
    {
    //delete from database
    }

if (isset($_POST['complete']))
    {
    //is_done in db set to 1
    }   

if (isset($_POST['add'])) 
    {
    //add to database
    }

if (isset($_POST['view']))
    {
    //view the tasks
    }



$tasks =  $conn -> query("SELECT * FROM tasks");

while ($row = $tasks->fetch_assoc()) {
    echo "<div>";
    echo "Task: " . htmlspecialchars($row["title"]) . "<br>";
    echo "</div><hr>";
}


if(isset($_POST['logout'])) {
    session_unset();
    session_destroy();
    header("Location: form_upgraded.php");
}

?>