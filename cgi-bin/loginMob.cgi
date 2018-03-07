#!/usr/bin/perl
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
my $cgi=new CGI;
require "utility.cgi";
#&printHeader("Login");
if(&getSession()){
    &printHeader("Utente");
}
else{
    &printHeader("Login");
}
&printForm;
&printFooter;
exit;
