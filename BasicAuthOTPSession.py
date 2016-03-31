#!/usr/bin/env python

import sys, os, sqlite3, hashlib, time

DB = '/tmp/otpsession.sqlite'
TIMELIMIT = 600
AUTHENTICATOR = "/usr/bin/pwauth"


def InitDB () :
  global conn
  global cursor
  global DB

  conn   = sqlite3.connect(DB, isolation_level=None)
  cursor = conn.cursor()

  sql = 'CREATE TABLE IF NOT EXISTS session \
           ( user text, passwdhash text, ip text, lastseen integer )'
  cursor.execute ( sql )


def CheckSession (c, user, passwdhash, ip) :
  global TIMELIMIT
  strtime  = "%d" % (int(time.time()) - TIMELIMIT)
  query = "SELECT user FROM session \
            WHERE user = ? \
              AND passwdhash = ? \
              AND ip = ? \
              AND lastseen > ?"
  c.execute ( query, (user, passwdhash, ip, strtime) )
  data = cursor.fetchone()
  if data is None:
    return False
  else:
    return True


def UpdateSession (c, user, passwdhash, ip) :
  query = "UPDATE session \
              SET lastseen = strftime('%s', 'now') \
            WHERE user = ? \
              AND passwdhash = ? \
              AND ip = ?"
  c.execute ( query, (user, passwdhash, ip) )


def AddSession ( c, user, passwdhash, ip) :
  query = "INSERT INTO session \
           VALUES ( ?, ?, ?, strftime('%s', 'now') )"
  c.execute ( query, (user, passwdhash, ip) )


def CleanSession ( c ):
  global TIMELIMIT
  
  strtime  = "%d" % (int(time.time()) - TIMELIMIT)
  query = "DELETE FROM session \
            WHERE lastseen < %s" % (strtime)
  c.execute ( query )
  
  
def Authenticate ( user, passwd ):
  global AUTHENTICATOR
  
  ret = os.system( "echo -e '%s\n%s' | %s" % (user, passwd, AUTHENTICATOR) )
  sys.stderr.write( "prog=%s, user=%s ret=%d \n" \
                     % (AUTHENTICATOR, user, ret) )
  
  if (ret == 0):
    return True
  else:
    return False


def main ():

  user   = sys.stdin.readline().strip()
  passwd = sys.stdin.readline().strip()
  ip     = os.getenv('IP', '0.0.0.0')
  
  m = hashlib.md5()
  m.update(passwd)
  passwdhash = m.hexdigest()
  
  InitDB ( )
  CleanSession ( cursor )
  
  if ( CheckSession ( cursor, user, passwdhash, ip ) ) :
    
    UpdateSession ( cursor, user, passwdhash, ip )
    conn.close()
    sys.exit(0)
  
  else:
    if Authenticate (user, passwd):
      AddSession ( cursor, user, passwdhash, ip )
      conn.close()
      sys.exit(0)
    else:
      sys.exit(1)
    
if ( __name__ == '__main__'): main()
