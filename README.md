# BasicAuthOTPSession
Simple Session Management for HTTP Basic Authentication with One-Time Password (OTP)

## The Issue
With HTTP Basic Authentication, the web browser caches login credentials and 
send them to the server during page requests. When a One-Time Password is
used as authentication (e.g. with "pwauth" and external authentication
module in Apache/HTTP Server), this becomes an issue since the same
credential is invalid after the first success (hence a "one-time password").
The net effect is that user gets asked for another authentication for every
page request, which sometime creates an illusion that their credentials
never works. 

## The Solution
The simple solution is to have a simple session management before the real
authenticator (e.g. "pwauth") that authenticates to whatever mechanism is
used for one-time password (e.g. RSA SecurID token). This simple code does
exactly that by wrapping the real authenticator (e.g. "pwauth"). Once an 
authentication succeed, the next request with the same credentials (and
other constraints) are deemed successfull without going through the real
authenticator with OTP until predefined amount of time. If no 'active'
request happens during the predefined time, the 'session' expires.

## Code Requirement
Python and with SQLite module


