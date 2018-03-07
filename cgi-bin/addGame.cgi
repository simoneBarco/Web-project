#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
require 'game_utility.cgi';
&printHeader("Nuovo/Modifica gioco");
my $page=new CGI;
my $tmpUser=&getSession();

 if(!($tmpUser eq 'admin@mail.com')){
     print '<h3 class="errori"> Per accedere a questa pagina &egrave; necessario effettuare il login come Amministratore!!</h3>';
     &printFooter;
 }
 else{
     &printFormG;
     &printFooter;
 }
