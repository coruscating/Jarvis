<?php
if(!empty($_POST['plotdata']) && !empty($_POST['filename'])){
	$data = $_POST['plotdata'];
	$filename = $_POST['filename'];
	$comment = $_POST['comment'];
	$dir = "/Dropbox/Quanta/Data/" . date('Y-m-d');
	mkdir($dir, 0775);
	$filename= $dir . '/' . $filename;
	if(file_exists($filename)){
		echo "File already exists!";
		exit(-1);
	}

	$file = fopen($filename, 'w');//creates new file
	fwrite($file, $comment);
	fwrite($file, $data);
	fclose($file);
	echo "File saved, " . strval(floatval(filesize($filename))/1000) . "kB";
}
else{
	echo "No file!";
}
?>

