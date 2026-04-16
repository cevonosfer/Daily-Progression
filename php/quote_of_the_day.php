
<?php
$quotes = file("C:\Users\cevhe\OneDrive\Desktop\quotes.txt" ,  FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
$random = $quotes[array_rand($quotes)];
?>


<!DOCTYPE html>
<html>
<head>
    <title>

    </title>
</head>

<body>

    <form action="" method="post">
        <header>
            <?php  echo $random  ?>
        </header>



    </form>

</body>
</html>


