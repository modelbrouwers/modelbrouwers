<?php


function GetDBSession()
{
  global $django_dbname, $django_dbuser, $django_dbpasswd;
  $dbSession = pg_connect("dbname={$django_dbname} user=${django_dbuser} password={$django_dbpasswd}");
  if (!$dbSession)
  {
    throw new Exception("cannot connect to DBMS: " . pg_last_error());
  }

  return $dbSession;
}


function GetDjangoUser()
{
    global $django_session_cookie;
    $djangoSessionID = $_COOKIE[$django_session_cookie];
    if(!$djangoSessionID){
      $djangoSessionID = $_COOKIE['sessionid'];
    }

    $dbSession = GetDBSession();
    $query =
      "SELECT u.username as username, u.email as email ".
      "  FROM users_user u, sessionprofile_sessionprofile sp" .
      " WHERE sp.session_key = '" . pg_escape_string($djangoSessionID) . "' " .
      "   AND u.id = sp.user_id
          AND u.is_active = True";
    $queryID = pg_query($dbSession, $query);

    if (!$queryID)
    {
      throw new Exception("Could not check whether user was logged in: " , pg_last_error());
    }

    $row = pg_fetch_array($queryID);
    if ($row)
    {
      return $row;
    }

    pg_close($dbSession);

    return null;
}

?>
