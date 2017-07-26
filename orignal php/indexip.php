<html>
<head>
  <link href="css/bootstrap.min.css" rel="stylesheet" type="text/css">
</head>
<body>
  <div class="container">
    <div class="row">
      <div class="col-md-9">
<?php
$search = isset($_GET['query']) ? $_GET['query'] : '';
@mysql_connect("localhost","root","bingo") or die(mysql_error());
mysql_select_db("_ip");
$query = mysql_query("SELECT * FROM search_engine WHERE Name LIKE '%$search%' OR Description LIKE '%$search%' OR Keywords LIKE '%$search%'");
?>
<?php
if(mysql_num_rows($query) >=1){
  while($a = mysql_fetch_array($query)){
    echo "<br> <a href={$a['Url']}>{$a['Name']}</a><br>{$a['Description']}&nbsp&nbsp {$a['Helpline_no']}<br>{$a['Phone_number']}<hr>\n";
  }
} else {
  echo "oh no! nothing was found.";
}
 ?>

</div>
</div>
</div>
</body>
</html>
