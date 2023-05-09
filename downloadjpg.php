<?php
set_time_limit(60);
if (isset($_GET['url'])) {
    $url = $_GET['url'];
   
        
        $cmd = "python download2.py ".(string)$url;
       
       
        $command = escapeshellcmd($cmd);
        $output = shell_exec($command);
        
            echo 'Download Successful';
            echo '<br>';
            echo $output;
        
}

?>
