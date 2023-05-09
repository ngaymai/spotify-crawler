<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $url = $_POST['url'];
    $file_extension = $_POST['fe'];

    if (!filter_var($url, FILTER_VALIDATE_URL)) {
        die('Invalid URL');
    }
    if (!preg_match('/^\.([a-zA-Z0-9]){3,4}$/i', $file_extension)) {
        die('Invalid file extension');
    }
   
    
    if ($file_extension == '.mp3'){
        $command = escapeshellcmd('python crawl.py mp3 '.$url);
        
    }
    elseif ($file_extension == '.jpg'){
        $command = escapeshellcmd('python crawl.py jpg '.$url);
        
    }
    $output = shell_exec($command);

    // Display the list of crawled URLs
    echo "<h1>Crawled URLs:</h1>";
    // echo $output;
    $arr = json_decode(str_replace("'", '"', $output), true);
    $url = array_pop($arr);
    // print_r($arr);
    // echo $url;
    // echo '<br>';
    foreach ($arr as $crawled_url) {
        echo '<a href="' . $crawled_url . '">' . $crawled_url . '</a> ';   
        if ($file_extension == '.mp3'){
            echo '<a href="downloadmp3.php?url=' .$crawled_url. '"><button>Download</button></a>';
            
        }
        elseif ($file_extension == '.jpg'){
            echo '<a href="downloadjpg.php?url=' .$crawled_url. '"><button>Download</button></a>';
            
        }
             
        echo '<br>';
    }
    if ($file_extension == '.mp3'){
        echo '<a href="download.php?url=' .$url. '"><button>Download</button></a>';
        
    }
    elseif ($file_extension == '.jpg'){
        $newurl = implode(", ", $arr);
        echo '<a href="downloadjpg.php?url='.$newurl.'"><button>Download</button></a>';
        
    }
    
  

}


?>

