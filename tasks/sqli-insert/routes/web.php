<?php

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;

Route::match(['get', 'post'], '/', function (Request $request) {
    $output = '';

    if ($request->isMethod('post')) {
        $username = $request->input('username', '');
        $email = $request->input('email', '');
        $password = $request->input('password', '');
        $sql = "INSERT INTO users (username,email,password) VALUES ('$username','$email','$password')";

        try {
            DB::statement($sql);
            $output = 'Insert succeeded';
        } catch (Throwable $exception) {
            $output = 'SQLite error: ' . $exception->getMessage();
        }
    }

    $rows = DB::select('SELECT username,email,password FROM users');
    return new Response(
        "<h1>Laravel sqli-insert</h1>"
        . "<form method='post'><input name='username'><input name='email'>"
        . "<input name='password'><button>Register</button></form>"
        . "<p>$output</p><pre>"
        . htmlspecialchars(print_r($rows, true))
        . '</pre>'
    );
});
