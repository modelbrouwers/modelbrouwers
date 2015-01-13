<?php
$m = 60*60*24*31;
$LIMIT_TIME = 6*$m; //about 6 months

define('IN_PHPBB', true);
$phpbb_root_path = (defined('PHPBB_ROOT_PATH')) ? PHPBB_ROOT_PATH : '../';
$phpEx = substr(strrchr(__FILE__, '.'), 1);
include($phpbb_root_path . 'common.' . $phpEx);

$topic_id = request_var('t', 0);

$sql = 'SELECT topic_last_post_time
		FROM '. TOPICS_TABLE .
		' WHERE topic_id = ' . $topic_id;
$result = $db->sql_query($sql);
$last_post_time = (int) $db->sql_fetchfield('topic_last_post_time'); //Unix timestamp
$db->sql_close();
$now = time(); //Unix timestamp

$difference = $now - $last_post_time;
if ($difference > $LIMIT_TIME){
	$months_total = (int) ($difference/$m);
	$years = (int) ($months_total/12);
	$months = (int) ($months_total % 12);

	$message = 'Dit topic is al meer dan ';

	if ($years != 0 and $months != 0){
		$message .= "$years jaar en $months ";
		if ($months == 1){
			$message .= "maand ";
		} else {
			$message .= "maanden ";
		}
		$message .= 'niet meer actief.';
	} elseif ($years != 0 and $months == 0) {
		$message .= "$years jaar niet meer actief.";
	} else {
		$message .= "$months maanden niet meer actief.";
	}

	$message .= ' Waarschijnlijk is het beter om de topicstarter een persoonlijk bericht (PB) te sturen in plaats van een reactie te plaatsen. Je kan wel een post plaatsen als die echt toegevoegde waarde heeft.';
} else {
	$message = "";
}

echo $message;
?>
