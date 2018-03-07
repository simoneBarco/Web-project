#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&destroySession;
&printHeader("Logout");

print '<h3>Logout effettuato!</h3>';
&printFooter;
exit;
