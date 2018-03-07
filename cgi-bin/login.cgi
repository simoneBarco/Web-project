#!/usr/bin/perl
use XML::LibXML;
use HTML::Entities;
use CGI;
use CGI::Session;
use CGI::Carp qw(fatalsToBrowser);
my $cgi=new CGI;
require "utility.cgi";

my $filedati="../data/user.xml";
my $parser=XML::LibXML->new();
my $doc=$parser->parse_file($filedati) || die();
my $root=$doc->getDocumentElement || die();

#encode_entities(
my $email=$cgi->param("email");
my $pwd=$cgi->param("pwd");

my @utenti=$root->getElementsByTagName("utente");
my $tmpUser="";
my $tmpPwd="";
my $ramo=0;

foreach $elemento (@utenti){
    $tmpUser=$elemento->findnodes("email")->get_node(1)->textContent;
    $tmpPwd=$elemento->findnodes("pwd")->get_node(1)->textContent;
    if(($tmpUser eq $email) && ($tmpPwd eq $pwd)){
        $ramo=1;
    }
}
if($ramo==1){
    &createSession($email,"bentornato.cgi");
    exit;
}
&printHeader("ERRORE Login");
print '
          <h3 class="errori">Email o Password non corrette!</h3>';
&printFooter;
exit;
