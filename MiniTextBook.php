<!DOCTYPE html>
<html>
    <head>

    </head>

    <body>
        
    <form action="" method="post">
        <label for="text">please enter a message</label>
        <input type="text" name="text" id="text">
        <button type="submit" name="submit">Submit</button>


    </form>
    </body>
</html>




<?php

    $message = trim($_POST['text']);
    $file = "messages.txt";
    $current = nl2br(file_get_contents($file));

    
    
    if ($message !== "") {
        file_put_contents($file , $message ."\n", FILE_APPEND );
        echo(nl2br((file_get_contents($file))));
    }
    else {echo $current;}

?>