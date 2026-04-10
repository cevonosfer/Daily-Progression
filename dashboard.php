<?php
session_start();
require 'config.php';
if (!isset($_SESSION['logged-in'])) {
    header("Location: login.php");
    exit();
}
?>

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
$task_name = trim($_POST['task'] ?? "");
$user_id = $_SESSION['user_id'];
$task_id = $_POST['task_id'] ?? "";

echo "welcome " . $_SESSION['username'];

if (isset($_POST['view']))
    {
        $tasks =  $conn -> query("SELECT * FROM tasks WHERE user_id=$user_id");
        while ($task = $tasks->fetch_assoc()) { ?>
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
            
    <?php }
    }
    
if(isset($_POST['delete'])) 
    {
    $prepared1 = $conn->prepare("DELETE FROM tasks WHERE id = ?");
    $prepared1->bind_param("i", $task_id);
    $prepared1->execute();   
    }

if(isset($_POST['complete']) && ($conn -> query("SELECT is_done FROM tasks WHERE id = $task_id")) != 'done' )
    {
    $prepared2 = $conn->prepare("DELETE FROM tasks WHERE id = ?");
    $prepared2->bind_param("i", $task_id);
    $prepared2->execute();
    }   

if(isset($_POST['add']) && !empty($task_name)) 
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