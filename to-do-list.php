<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        <form method="POST">
            <label for="ntask" id="ntask">New Task</label>
            <input  name="ntask" >
            <button type="submit" name="action" value="add">Add Task</button>

        </form>
    </body>
</html>



<?php
    $task = trim($_POST['ntask'] ?? "");
    $action = $_POST['action'] ?? "";
    $list = "list.json";
    $decoded = json_decode(file_get_contents($list) , true);

?>

   



<?php   if ($action == 'add' && $task !== "") 
        {
        $decoded[] = 
        ["text" => $task,
        "completed" => false];

        file_put_contents($list, json_encode($decoded, JSON_PRETTY_PRINT));

        }
        
            

    if ($action == 'delete') 
        {
        $index = $_POST['index'];
        unset($decoded[$index]);
        $decoded = array_values($decoded);
        file_put_contents($list , json_encode($decoded, JSON_PRETTY_PRINT));
            
            
        }
    if ($action == 'complete') 
        {
        $index = $_POST['index'];
        $decoded[$index]['completed'] = true;
        file_put_contents($list , json_encode($decoded, JSON_PRETTY_PRINT));



        }
    if ($action == 'show') 
        {

        }
    ?>

     <?php foreach ($decoded as $index => $single_task): ?>
        <form action="" method="POST">
        <input type="hidden" name="index" value="<?= $index ?>">
        <?php echo(htmlspecialchars($single_task['text'])); ?>
        <button type="submit" name="action" value="delete">Delete</button>
        <button type="submit" name="action" value="complete">Mark Complete</button>
        <?php if ($decoded[$index]['completed'] == true): ?>
            <?php echo ("completed") ?>
        <?php endif ?> 
        </form>
    <?php endforeach; ?>


 

            
    
    




