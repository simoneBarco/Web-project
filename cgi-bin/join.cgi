#!/usr/bin/perl
use CGI; # importa la libreria CGI
use XML::LibXML; # importa LibXML
use HTML::Entities;
require 'utility.cgi';
my $page=new CGI; # crea un oggetto CGI
#Recupera i dati inviati
my $nome=$page->param('nome');
utf8::encode($nome);
my $cognome=$page->param('cognome');
utf8::encode($cognome);
my $email=$page->param('email');
utf8::encode($email);
my $nick=$page->param('nickname');
utf8::encode($nick);
my $pw1=$page->param('pw1');
utf8::encode($pw1);
my $pw2=$page->param('pw2');
utf8::encode($pw2);

#verifica validità
my $snome=$nome; #togliere gli spazi nel controllo
$snome=~s/ //g;
my $scognome=$cognome;
$scognome=~s/ //g;
my $semail=$email;
$semail=~s/ //g;
my $snick=$nick;
$snick=~s/ //g;
my $spw1=$pw1;
$spw1=~s/ //g;
my $spw2=$pw2;
$spw2=~s/ //g;
my $check=0;#=1 se l email è gia presente
$nome=~s/&/&amp;/g;
$nome=~s/>/&gt;/g;
$nome=~s/</&lt;/g;

$cognome=~s/&/&amp;/g;
$cognome=~s/>/&gt;/g;
$cognome=~s/</&lt;/g;

$nick=~s/&/&amp;/g;
$nick=~s/>/&gt;/g;
$nick=~s/</&lt;/g;

$pw1=~s/&/&amp;/g;
$pw1=~s/>/&gt;/g;
$pw1=~s/</&lt;/g;

$pw2=~s/&/&amp;/g;
$pw2=~s/>/&gt;/g;
$pw2=~s/</&lt;/g;


if(($spw1 eq $spw2)&&($snome ne "")&&($scognome ne "")&&($semail ne "")&&($spw1 ne "")&&($email=~ m/^([\w\-\+\.]+)@([\w\-\+\.]+)\.([\w\-\+\.]+)$/)&&($snick ne "")){
	my $filedati="../data/user.xml";
	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file($filedati) || die("fail parser");
	my $root=$doc->getDocumentElement || die("fail radice");


	my @utenti = $root->getElementsByTagName('utente');
	foreach $elemento (@utenti){
		if($elemento->findnodes("email")->get_node(1)->textContent eq $email){
			$check=1;
		}
	}

	if($check==0){#è possibile registrare
		my $frammento ="<utente>
						<nome>".$nome."</nome>
						<cognome>".$cognome."</cognome>
						<nickname>".$nick."</nickname>
						<email>".$email."</email>
						<pwd>".$pw1."</pwd>
		</utente>";
		my $nodo = $parser->parse_balanced_chunk($frammento)||die("fail frammento");
		my $padre=$root;
		$padre->appendChild($nodo) || die ("fail append");
		open(OUT,">$filedati");
		print OUT $doc->toString;
		close(OUT);
		&createSession($email,"regEff.cgi");
	}
	else{
		&printHeader("ERRORE Registrazione");
		print "<h3 class=\"errori\">Non &egrave; possibile registrarsi pi&uacute volte utilizzando la stessa email!</h3>";
		print '<a href="registrazione.cgi">Indietro</a>';
		&printFooter;
	}
}
else{
	&printHeader("ERRORE Registrazione");


	#mostra tutti gli errrori del form
	print "<h3 class=\"errori\">Ricontrollare i dati!</h3>";
	if($snome eq "Inserirenome" || $snome eq ""){
		print "<h3 class=\"errori\">Nome &egrave; un campo obbligatorio!</h3>";
	}
	if($scognome eq "Inserirecognome" || $scognome eq ""){
		print "<h3 class=\"errori\">Cognome &egrave; un campo obbligatorio!</h3>";
	}
	if($snick eq "Inserirenickname" || $snick eq ""){
		print "<h3 class=\"errori\">Nickname &egrave; un campo obbligatorio!</h3>";
	}
	if($semail eq "InserireE-mail" || $semail eq ""){
		print "<h3 class=\"errori\">E-mail &egrave; un campo obbligatorio!</h3>";
	}
	if(!($email=~ m/^([\w\-\+\.]+)@([\w\-\+\.]+)\.([\w\-\+\.]+)$/)){
		print "<h3 class=\"errori\">Indirizzo email non valido!</h3>";
	}
	if(($spw1 eq "" )||($spw2 eq "Reinserirepassword" || $spw2 eq "")){
		print "<h3 class=\"errori\">Password &egrave; un campo obbligatorio!</h3>";
	}
	if($spw1 ne $pw2){
		print "<h3 class=\"errori\">Le password devono coincidere!</h3>";
	}
	print '<a href="registrazione.cgi">Indietro</a>';
}
&printFooter;
# fine pagina HTML
exit;
