<?php
try {$conn = mysqli_connect("localhost" , "root" , "" , "login");}
catch (mysqli_sql_exception) {echo "connection error";}
?>