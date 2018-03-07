#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&printHeader("Amministrazione");
my $page=new CGI;
my $tmpUser=getSession();

if(!($tmpUser eq 'admin@mail.com')){
    print '<h3 class="errori"> Per accedere a questa pagina &egrave; necessario effettuare il login come Amministratore!!</h3>';
    &printFooter;
}
else{
    print '<h2>Selezionare un\'operazione da eseguire</h2>
                <a tabindex="26" href="addGame.cgi">Inserisci nuovo gioco</a><br />
                <a tabindex="27" href="addEvent.cgi">Inserisci nuovo evento</a><br />';
    &printFooter;
}
exit;
