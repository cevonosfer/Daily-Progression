<?php session_start(); ?>

<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        
        <form action="" method="POST">
        <input type="text" name="task">
        <button name="add">Add Task</button>
        <button name="view">View Tasks</button>
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
$task_name = trim($_POST['task'] ?? "");
$user_id = $_SESSION['user_id'];

try {$conn = mysqli_connect($db_server , $db_user , $db_password , $db_name);}
catch (mysqli_sql_exception) {echo "connection error";}
$is_completed = $conn -> query("SELECT is_done FROM tasks");


echo "welcome" . $_SESSION['username'];

if (isset($_POST['view']))
    {
        $tasks =  $conn -> query("SELECT * FROM tasks WHERE user_id=$user_id");
        while ($row = $tasks->fetch_assoc()) { ?>
        <?php foreach ($tasks as $task): ?>
            <div>
                <?php echo htmlspecialchars($task['name']); ?>
                <?php echo htmlspecialchars($task['is_done']); ?>
                
                <form method="POST" style="display:inline;">
                    <input type="hidden" name="task_id" value="<?php echo $task['id']; ?>">
                    <button type="submit" name="complete">Complete</button>
                </form>
                
                <form method="POST" style="display:inline;">
                    <input type="hidden" name="task_id" value="<?php echo $task['id']; ?>">
                    <button type="submit" name="delete" >Delete</button>
                </form>
            </div>
            <?php endforeach; ?>
            <?php }
    }
    $task_id = $_POST['task_id'];
    
if (isset($_POST['delete'])) 
    {
    $conn -> query("DELETE FROM tasks WHERE id = $task_id ");
    }

if (isset($_POST['complete']) && ($conn -> query("SELECT is_done FROM tasks WHERE id = $task_id")) != 'done' )
    {
    $conn -> query("UPDATE tasks SET is_done='done' WHERE id = $task_id");
    }   

if (isset($_POST['add']) && !empty($task_name)) 
    {
    {
    $prepared = $conn->prepare("INSERT INTO tasks (name, user_id) VALUES (?, ?)");
	$prepared->bind_param("si", $task_name, $user_id);
	$prepared->execute();
    }
    }


if(isset($_POST['logout'])) {
    session_unset();
    session_destroy();
    header("Location: form_upgraded.php");
}

?>