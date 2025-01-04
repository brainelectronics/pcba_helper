<?php 
session_start(['cookie_lifetime' => 86400,]);
require_once __DIR__ . '/auth.php';

if (is_post_request()) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if (login($username, $password)) {
        unset($_SESSION['errors']['login']);
        redirect_to('../overview.php');
    } else {
        $errors['login'] = "Invalid username or password";
        // $errors['login2'] = "keep this after successfull login";
        redirect_with('../index.php', ['errors' => $errors]);
    }
} else if (is_get_request()) {
    redirect_to('../index.php');
}
?>
