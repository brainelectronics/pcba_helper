<?php
session_start(['cookie_lifetime' => 86400,]);
require_once __DIR__ . '/auth.php';
logout();
?>
