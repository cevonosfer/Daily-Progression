<?php session_start(); ?>

<!DOCTYPE html>
<html>
    <head>

    </head>
    <body>
        
        <form action="" method="POST">
        <button name="logout">Log Out</button>
        </form>
    </body>
</html>


<?php

    echo "welcome" . $_SESSION['username'];
    if(isset($_POST['logout'])) {
        session_unset();
        session_destroy();
        header("Location: form_upgraded.php");
    }

?>