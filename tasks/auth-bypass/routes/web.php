<?php

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;

Route::match(['get', 'post'], '/', function (Request $request) {
    $message = '';

    if ($request->isMethod('post')) {
        $username = $request->input('username', '');
        $password = $request->input('password', '');
        $sql = "SELECT * FROM users WHERE username='$username' AND password='$password' LIMIT 1";

        try {
            $user = DB::select($sql);
            $message = $user
                ? 'Login successful. FLAG: ' . DB::table('secret_flag')->value('flag')
                : 'Invalid credentials';
        } catch (Throwable $exception) {
            $message = 'SQLite error: ' . $exception->getMessage();
        }

        return new Response(
            "<h1>Laravel auth-bypass SQLi</h1>"
            . "<p>Query: <code>$sql</code></p><p>$message</p>"
        );
    }

    return new Response(
        '<h1>Laravel auth-bypass SQLi</h1>'
        . '<form method="post"><input name="username"><input name="password">'
        . '<button>Login</button></form>'
    );
});
