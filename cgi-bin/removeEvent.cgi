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
    &printFooter;
}
else{
    my $id= $page->param('id');
    my $confe= $page->param('conferma');

    my $fileXML="../data/events.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    if($confe eq "Si"){
        &printHeader("Cancellazione Evento");
        my $id2= $session->param('idelim');

        my $elemElim= $doc->findnodes("//event[ID=$id2]")->get_node(1);
        my $file= $elemElim->findnodes("image")->get_node(1)->textContent;
        if($file ne "../immagini/noImg.jpg"){
            $file= substr $file, 3;
            $file= "../public_html/$file";
            unlink $file;
        }
        my $parent= $elemElim->parentNode;
        $parent->removeChild($elemElim);

        open(OUT, ">$fileXML");
        print OUT $doc->toString;
        close (OUT);

        $session->clear(["~logged-in", "idelim"]);
        print '<h3>CANCELLAZIONE EFFETTUATA</h3>
                <a href="eventi.cgi">Torna alla pagina degli eventi</a>';

        &printFooter;

    }
    else{
        &printHeader("Conferma eliminazione Evento");
        $session->param("idelim", $id);
        my $titEvent= $doc->findnodes("//event[ID=$id]/title")->get_node(1)->textContent;
        my $dataEvent= $doc->findnodes("//event[ID=$id]/date")->get_node(1)->textContent;
        print'<form action="removeEvent.cgi" method="get">
                    <fieldset>
                        <legend>Confermi la cancellazione?</legend>
                        Nome evento: '.$titEvent.'<br />
                        Previsto in data: '.$dataEvent.'<br/>
                        <input tabindex="26" type="submit" value="Si" name="conferma"/>
                        <a tabindex="27" href="eventi.cgi?id='.$id.'">No</a>
                    </fieldset>
        </form>';
        &printFooter;
    }
}
1;
