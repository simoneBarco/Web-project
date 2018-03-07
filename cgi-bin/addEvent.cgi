#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
require "event_utility.cgi";
&printHeader("Nuovo/Modifica evento");
my $page=new CGI;
my $tmpUser=&getSession();

if(!($tmpUser eq 'admin@mail.com')){
    print '<h3 class="errori"> Per accedere a questa pagina &egrave necessario effettuare il login come Amministratore!!</h3>';
    &printFooter;
}
else{
    &printFormE;
    &printFooter;
}
