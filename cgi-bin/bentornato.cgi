#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&printHeader("Bentornato");
print '<h3> Bentornato ';
my $tmpUser=getSession();


if($tmpUser eq 'admin@mail.com'){
    print 'Amministratore';
}
else{
    print $tmpUser;
}
print'</h3>';
&printFooter;
exit;
