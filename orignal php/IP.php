<html>
<head>
<title>IP</title>
<link type="text/css" rel="stylesheet" href="ip2.css" />
<script src="jquery.js"></script>
<style>
A {FONT-FAMILY :arial}
P {FONT-FAMILY :Times New Roman}
</style>
</head>
<body>
<div class="main-box">
<ul id="menu">
<li><a href="http://mail.google.com">Gmail</a></li>
<li><a href="http://www.facebook.com">facebook</a></li>
<li><a href="http://www.youtube.com">Youtube</a></li>
<li><a href="http://punjab.chitkara.edu.in">Chalkpad</a></li>
<li><a href="http://www.yahoo.in">Yahoo</a></li>
</ul>
</div>
<div class="content">
<br><br><br><br>
<center>
<table cellspacing=0 cellpadding=0 border=0>
</tbody>
<tr>
<td>
<p style="font-size:85;"><b>
<font color="blue">B</font>
<font color="red">I</font>
<font color="orange">N</font>
<font color="green">G</font>
<font color="purple">O</font>
</p></b></td></tr><tbody></table><br>

<form action="indexip.php" id="searchBox" method="get">

<input type='text' id='searchBox1' name="query" placeholder="search" size="55" style="height:35px"><br><br>
<input type="submit" value="search" id='searchButton' disabled>
</form>
<script>
$(document).ready(function()
{
   $('#searchBox1').keyup(function()
   {
      if($(this).val() == '')
      {
        $('#searchButton').attr('disabled', true);
      }
      else
      {
        $('#searchButton').removeAttr('disabled');
      }

   });
});
</script>
</body>
</html>
