#!/usr/bin/perl
use CGI;
use CGI::Session();
use CGI::Push qw(:standard);
use XML::LibXML;
use Encode qw(decode encode);
use CGI::Carp qw(fatalsToBrowser);
use POSIX qw(strftime);

require 'utility.cgi';
require 'event_utility.cgi';

my $page= new CGI;

$session= CGI::Session->load() or die "sessione non trovata";

my $idComm= $session->param('idComm');
my $usr= &getSession();
my $dataEora= strftime "%d-%m-%Y, %H:%M", localtime;
my $testoC= $page->param("testoC");
$testoC=~s/&/&amp;/g;
$testoC=~s/>/&gt;/g;
$testoC=~s/</&lt;/g;
$testoC=~s/\n/<br\/>/g;



my $fileXML= "../data/user.xml";
my $parser= XML::LibXML->new();
my $doc= $parser->parse_file($fileXML) || die("fail parser");
my $elem= $doc->findnodes("//utente[email='$usr']")->get_node(1);
my $nickname= $elem->findnodes("nickname")->get_node(1)->textContent;

$fileXML= "../data/events.xml";
$doc= $parser->parse_file($fileXML) || die("fail parser");
my $event= $doc->findnodes("//event[ID='$idComm']")->get_node(1);
my $tit= $event->findnodes("title")->get_node(1)->textContent;
&printHeader("Aggiunta commento $tit");
my $comment= $event->findnodes("comments")->get_node(1);
if($comment){
    # QUI <comments> c'e gia quindi devo solo aggiungere il pezzo <comment>
    #padre <comments>
    my @num= $comment->getElementsByTagName("comment");
    my $nrMax=0;
    foreach $n (@num){
        my $nCurr= $n->findnodes("nr")->get_node(1)->textContent;
        if($nCurr > $nrMax){
            $nrMax= $nCurr;
        }
    }
    my $nr= $nrMax+1;
    my $frammento= "<comment>
                        <nr>".$nr."</nr>
                        <nickname>".$nickname."</nickname>
                        <dataEora>".$dataEora."</dataEora>
                        <testo>".$testoC."</testo>
                    </comment>";
    my $nodo= $parser->parse_balanced_chunk($frammento) || die("fail frammento");
    $comment->appendChild($nodo) || die("fail append");
    open(OUT, ">$fileXML");
    print OUT $doc->toString;
    close (OUT);

    print '<h3>AGGIUNTO COMMENTO</h3>';
    $session->clear(["~logged-in", "idComm"]);
    &printFooter;
}
else{
    #QUI <comments> non c'e quindi devo aggiungere anche <comments>
    #al padre <event>
    my $frammento= "<comments>
                        <comment>
                            <nr>1</nr>
                            <nickname>".$nickname."</nickname>
                            <dataEora>".$dataEora."</dataEora>
                            <testo>".$testoC."</testo>
                        </comment>
                    </comments>";
    my $nodo= $parser->parse_balanced_chunk($frammento) || die("fail frammento");
    $event->appendChild($nodo) || die("fail append");
    open(OUT, ">$fileXML");
    print OUT $doc->toString;
    close (OUT);

    print '<h3>AGGIUNTO COMMENTO</h3>';
    &printFooter;
}

$page->end_html;
exit;
