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
    my $id= $page->param('id');
    my $ty= $page->param('ty');
    my $confe= $page->param('conferma');

    my $fileXML="";
    if($ty eq 'gpc' || $ty eq 'cpc'){
        $fileXML="../data/pc_games.xml";
    }
    if($ty eq 'gxbox' || $ty eq 'cxbox'){
        $fileXML="../data/xbox_games.xml";
    }
    if($ty eq 'gps4' || $ty eq 'cps4'){
        $fileXML="../data/ps4_games.xml";
    }
    if($ty eq 'gnin' || $ty eq 'cnin'){
        $fileXML="../data/nintendo_games.xml";
    }
    my $parser= XML::LibXML->new();
    if($confe eq "Si"){
        &printHeader("Cancellazione Gioco/Console");
        my $id2= $session->param('idelim');
        my $ty2= $session->param('tyelim');
        if($ty2 eq 'gpc' || $ty2 eq 'cpc'){
            $fileXML="../data/pc_games.xml";
        }
        if($ty2 eq 'gxbox' || $ty2 eq 'cxbox'){
            $fileXML="../data/xbox_games.xml";
        }
        if($ty2 eq 'gps4' || $ty2 eq 'cps4'){
            $fileXML="../data/ps4_games.xml";
        }
        if($ty2 eq 'gnin' || $ty2 eq 'cnin'){
            $fileXML="../data/nintendo_games.xml";
        }
        if($ty2 eq ""){
            print 'nessuna categoria selezionata';
            exit;
        }
        my $doc= $parser->parse_file($fileXML) || die("fail parser");
        my $elemElim= $doc->findnodes("//game[ID=$id2]")->get_node(1);
        my $file= $elemElim->findnodes("image")->get_node(1)->textContent;
        #CONTROLLARE CHE IL FILE NON SIA noImg.jpg
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
        $session->clear(["~logged-in", "tyelim"]);
        print '<h3>CANCELLAZIONE EFFETTUATA</h3>
                <a href="giochi.cgi?ty='.$ty2.'">Torna alla sezione</a>';

        &printFooter;

    }
    else{
        &printHeader("Conferma eliminazione Gioco/Console");
        $session->param("idelim", $id);
        $session->param("tyelim", $ty);
        my $doc= $parser->parse_file($fileXML) || die("fail parser");
        my $titGame= $doc->findnodes("//game[ID=$id]/title")->get_node(1)->textContent;
        my $catGame= $doc->findnodes("//game[ID=$id]/category")->get_node(1)->textContent;
        my $catGame2= "";
        if($catGame eq "gpc"){
            $catGame2="Gioco PC";
        }
        if($catGame eq "gxbox"){
            $catGame2="Gioco XBox";
        }
        if($catGame eq "gps4"){
            $catGame2="Gioco PS4";
        }
        if($catGame eq "gnin"){
            $catGame2="Gioco Nintendo";
        }
        if($catGame eq "cpc"){
            $catGame2="Accessorio PC";
        }
        if($catGame eq "cxbox"){
            $catGame2="Console XBox";
        }
        if($catGame eq "cps4"){
            $catGame2="Console PS4";
        }
        if($catGame eq "cnin"){
            $catGame2="Console Nintendo";
        }
        print'<form action="removeGame.cgi" method="get">
                    <fieldset>
                        <legend>Confermi la cancellazione?</legend>
                        Titolo: '.$titGame.'<br />
                        Categoria: '.$catGame2.'<br />
                        <input tabindex="26" type="submit" value="Si" name="conferma"/>
                        <a tabindex="27" href="giochi.cgi?ty='.$catGame.'">No</a>
                    </fieldset>
        </form>';
        &printFooter;
    }
}
1;
