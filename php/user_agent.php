<?php

if (str_contains($_SERVER['HTTP_USER_AGENT'], 'Chrome')) {
	echo 'You are using chrome';
}

echo $_SERVER['HTTP_USER_AGENT'];

?>