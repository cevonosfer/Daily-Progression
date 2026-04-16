<!DOCTYPE html>
<html>
<head>
    <title>


    </title>
</head>

<body>
    <form action="calculator.php" method="post">
        <label for="number1">Enter number 1 : </label>
        <input type="number" id="number1" name="number1"> <br>

        <label for="number2">Enter number 2 : </label>
        <input type="number" id="number2" name="number2"> <br>

        <label for="operation">Select a operation </label>
        <select name="operation" id="operation">
            <option value="add">add</option>
            <option value="substract">substract</option>
            <option value="multiply">multiply</option>
            <option value="divide">divide</option>
        </select>
            <button type="calculate">calculate</button>
        </form>

</body>
</html>




<?php


$number1 = trim($_POST['number1']);
$number2 = trim($_POST['number2']);
$operation = trim($_POST['operation']);


switch ($operation)  {

    case "add"; 
        echo ("Your result is : " . $number1 + $number2);
    break;
    case "substract";
        echo ("Your result is : " . $number1 - $number2);
    break;
    case "multiply";
        echo ("Your result is : " . $number1 * $number2);
    break;
    case "divide";
        {   try {echo ("Your result is : " . $number1 / $number2);}
            catch(DivisionByZeroError) {echo "cannnot divide by zero";}}
        
        
    break;

}









?>