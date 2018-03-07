#!/usr/bin/perl
use CGI;
use XML::LibXML;
use CGI::Session();
require "utility.cgi";

my $page= new CGI;
$session= CGI::Session->load() or die "sessione non trovata";


my $tmpUser= getSession();
if($tmpUser ne 'admin@mail.com'){
    &printHeader("ERRORE autenticazione");
    print '<h3 class="errori">Per accedere a questa pagina &egrave necessario il login come Amministratore!</h3>';
    print $page->end_html;
}
else{
    my $idE= $page->param('idEvent');
    my $idC= $page->param('idComm');
    my $confe= $page->param('conferma');

    my $fileXML="../data/events.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    if($confe eq "Si"){
        my $idE2= $session->param('idEelim');
        my $idC2= $session->param('idCelim');
        &printHeader("Cancellazione commento");

        my $elemElim= $doc->findnodes("(//event[ID=$idE2])/comments/comment[nr=$idC2]")->get_node(1);
        my @comments= $doc->findnodes("(//event[ID=$idE2])/comments/comment");
        my $comment= @comments-1;
        if($comment != 0){
            #se ci sono altri commenti
            my $parent= $elemElim->parentNode;
            $parent->removeChild($elemElim);
        }
        else{
            #se non ci sono piu' commenti
            my $parent1= $elemElim->parentNode;
            my $parent2= $parent1->parentNode;
            $parent2->removeChild($parent1);
        }


        open(OUT, ">$fileXML");
        print OUT $doc->toString;
        close (OUT);

        print '<h3>CANCELLAZIONE EFFETTUATA</h3>';
        $session->clear(["~logged-in", "idEelim"]);
        $session->clear(["~logged-in", "idCelim"]);
        &printFooter;

    }
    else{
        &printHeader("Conferma eliminazione commento");
        $session->param("idEelim", $idE);
        $session->param("idCelim", $idC);
        my $textComment= $doc->findnodes("(//event[ID=$idE])/comments/comment[nr=$idC]/testo")->get_node(1)->textContent;
        my $usrComm= $doc->findnodes("(//event[ID=$idE])/comments/comment[nr=$idC]/nickname")->get_node(1)->textContent;
        my $dataEoraComm= $doc->findnodes("(//event[ID=$idE])/comments/comment[nr=$idC]/dataEora")->get_node(1)->textContent;
        print'<form action="removeComment.cgi" method="get">
                    <fieldset>
                        <legend>Confermi la cancellazione?</legend>
                        Testo: '.$textComment.'<br/>
                        Inviato da: '.$usrComm.'<br/>
                        In data: '.$dataEoraComm.'<br/>
                        <input tabindex="26" type="submit" value="Si" name="conferma"/>
                        <a tabindex="27" href="eventi.cgi?id='.$idE.'">No</a>
                    </fieldset>
        </form>';
        &printFooter;
    }
}
