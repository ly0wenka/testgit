<?php
// Accept password from CLI arg or env var
$password = null;
if (isset($argv[1]) && strlen($argv[1]) > 0) {
    $password = $argv[1];
} elseif (getenv('PASSWORD')) {
    $password = getenv('PASSWORD');
} else {
    fwrite(STDERR, "Usage: php hash.php <password>\nOr set env var PASSWORD.\n");
    exit(2);
}

require_once __DIR__ . '/class-phpass.php';

// WordPress uses PasswordHash with iteration count 8 and portable hashes true
$wp_hasher = new PasswordHash(8, true);
$hash = $wp_hasher->HashPassword($password);

// Print the hash only
echo $hash . PHP_EOL;
