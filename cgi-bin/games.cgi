#!/usr/bin/perl
use CGI;
use CGI::Session();
use XML::LibXML;
use HTML::Entities;
use File::Basename;

use CGI::Carp qw(fatalsToBrowser);
require 'utility.cgi';
require 'game_utility.cgi';

my $page=new CGI;
#recupero dati
$session= CGI::Session->load() or die "sessione non trovata";

my $titolo= $page->param('title');
utf8::encode($titolo);
my $cat= $page->param('cat');
my $mant= $page->param('mant'); #SERVE PER VEDERE SE VOGLIO MANTERE L'IMMAGINE O NO
#PRIMA DI PRENDERE IMAGE DEVO CONTROLLARE CHE NON SI VOGLIA TENERE L'IMMAGINE PRECEDENTE (SOLO SU MODIFICA)
my $filename= $page->param('image');
my $noImg="../immagini/noImg.jpg";
my $boolImg=0; #0=immagine valida 1=immagine non valida
if ($filename eq ""){
    $boolImg=1;
}
my $id2= $session->param('idg');
my $idg=0;
if(!$id2){
    $idg=1;
}
my $sizef= -s $filename;
my $extension3= substr $filename, -3;
if($mant ne "si" && ($sizef > 3072000 || ($extension3 && $extension3 ne "jpg" && $extension3 ne "png" && $extension3 ne "bmp"))){ #controllo per dimensione file ed estensione
    &printHeader("ERRORE Gioco/Console");
    print '<h3 class="errori">ERRORE</h3>';
    print '<h3 class="errori">formato non supportato o file troppo grande!!</h3>';
    if(!$idg){
        print'<a id="err" href="addGame.cgi?id='.$id2.'&amp;ty='.$cat.'">Torna indietro</a>';
    }
    else{
        print'<a id="err" href="addGame.cgi">Torna indietro</a>';
    }
    &printFooter;
    exit;
}

my $day= $page->param('day');
if($day <10){
    $day= '0'.$day;
}
my $mon= $page->param('month');
if($mon < 10){
    $mon= '0'.$mon;
}
my $year= $page->param('year');

my $date= $day.'-'.$mon.'-'.$year;
my $prez= $page->param('price');

my $desc= $page->param('desc');
utf8::encode($desc);

my $stitolo= $titolo;
$stitolo=~s/ //g;
$titolo=~s/&/&amp;/g;
$titolo=~s/>/&gt;/g;
$titolo=~s/</&lt;/g;

my $sprez= $prez;
$sprez=~s/ //g;
my $sdesc= $desc;
$sdesc=~s/ //g;
$desc=~s/&/&amp;/g;
$desc=~s/>/&gt;/g;
$desc=~s/</&lt;/g;
$desc=~s/\n/&#xD;/g;


if(($stitolo ne "") && ($sprez ne "") && ($sprez=~m /^([0-9]+.[0-9]{1,}$)/) && ($sdesc ne "")){
    if($mant ne "si" && $boolImg==0){
        $CGI::POST_MAX= 1024*3000;
        my $safe_filename_characters = "a-zA-Z0-9_.-";
        my $up_dir="";
        if($filename eq "noImg.jpg"){
            $up_dir="../public_html/immagini";
        }
        if($cat eq "gpc" || $cat eq "cpc"){
            $up_dir="../public_html/immagini/games/pc";
        }
        if($cat eq "gxbox" || $cat eq "cxbox"){
            $up_dir="../public_html/immagini/games/xbox";
        }
        if($cat eq "gps4" || $cat eq "cps4"){
            $up_dir="../public_html/immagini/games/ps4";
        }
        if($cat eq "gnin" || $cat eq "cnin"){
            $up_dir="../public_html/immagini/games/nintendo";
        }
        if($filename ne ""){
            my ($name, $path, $extension)= fileparse($filename, '.*');

            $filename= $name.$extension;
            $filename=~ tr/ /_/;
            $filename=~ s/[^$safe_filename_characters]//g;

            if($filename =~ /^([$safe_filename_characters]+)$/ ){
                $filename = $1;
            }
            else{
                die "Filename contains invalid characters";
            }
            my $upload_filehandle = $page->upload("image");

            open(UPLOADFILE, ">$up_dir/$filename") or die "$!";
            binmode UPLOADFILE;

            while (<$upload_filehandle>){
                print UPLOADFILE;
            }
            close UPLOADFILE;
        }
    }


    #accesso al file XML
    my $fileXML="";
    if($cat eq 'gpc' || $cat eq 'cpc'){
        $fileXML="../data/pc_games.xml";
    }
    if($cat eq 'gxbox' || $cat eq 'cxbox'){
        $fileXML="../data/xbox_games.xml";
    }
    if($cat eq 'gps4' || $cat eq 'cps4'){
        $fileXML="../data/ps4_games.xml";
    }
    if($cat eq 'gnin' || $cat eq 'cnin'){
        $fileXML="../data/nintendo_games.xml";
    }

    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");

    my @games= $root->getElementsByTagName("game");
    if(!$id2){
        my $idMax=0;
        foreach $elemento (@games){
            my $idCurr= $elemento->findnodes("ID")->get_node(1)->textContent;
            my $tit2= $elemento->findnodes("title")->get_node(1)->textContent;
            my $tit3= $titolo;
            $tit3=~s/ //g;
            $tit3=lc $tit3;
            $tit2=~s/ //g;
            $tit2=lc $tit2;
            if($tit3 eq $tit2){
                &printHeader("ERRORE Gioco/Console");
                print '<h3 class="errori">ERRORE</h3>
                        <h3 class="errori">Titolo gi&agrave; presente per questa categoria!</h3>';
                if(!$idg){
                    print'<a id="err" href="addGame.cgi?id='.$id2.'&amp;ty='.$cat.'">Torna indietro</a>';
                }
                else{
                    print'<a id="err" href="addGame.cgi">Torna indietro</a>';
                }
                &printFooter;
                exit;
            }
            if($idCurr > $idMax){
                $idMax= $idCurr;
            }
        }
        my $newID= $idMax+1;
        my $frammento="";
        if($boolImg == 0){
            if($cat eq "gpc" || $cat eq "cpc"){
                $filename="../immagini/games/pc/$filename";
            }
            if($cat eq "gxbox" || $cat eq "cxbox"){
                $filename="../immagini/games/xbox/$filename";
            }
            if($cat eq "gps4" || $cat eq "cps4"){
                $filename="../immagini/games/ps4/$filename";
            }
            if($cat eq "gnin" || $cat eq "cnin"){
                $filename="../immagini/games/nintendo/$filename";
            }
            $frammento= "<game>
                                <ID>".$newID."</ID>
                                <title>".$titolo."</title>
                                <category>".$cat."</category>
                                <description>".$desc."</description>
                                <image>".$filename."</image>
                                <date>".$date."</date>
                                <price>".$prez."</price>
            </game>";
        }
        else{
            $frammento= "<game>
                                <ID>".$newID."</ID>
                                <title>".$titolo."</title>
                                <category>".$cat."</category>
                                <description>".$desc."</description>
                                <image>".$noImg."</image>
                                <date>".$date."</date>
                                <price>".$prez."</price>
            </game>";
        }

        my $nodo= $parser->parse_balanced_chunk($frammento, 'UTF-8') || die("fail frammento");
        my $padre= $root;
        $padre->appendChild($nodo) || die("fail append");
        open(OUT, ">$fileXML");
        print OUT $doc->toString;
        close (OUT);

        &printHeader("Caricamento Gioco/Console");
        print '<h3>CARICAMENTO AVVENUTO</h3>
                <a href="giochi.cgi?id='.$newID.'&amp;ty='.$cat.'">';
                if($cat eq "gpc" || $cat eq "gxbox" || $cat eq "gps4" || $cat eq "gnin"){
                    print'Vai alla pagina del gioco</a>';
                }
                if($cat eq "cpc"){
                    print'Vai alla pagina dell\'accessorio</a>';
                }
                if($cat eq "cxbox" || $cat eq "cps4" || $cat eq "cnin"){
                    print'Vai alla pagina della console</a>';
                }
                &printFooter;
    }
    else{
        my $elemM= $doc->findnodes("//game[ID=$id2]")->get_node(1);
        my $frammento="";
        if($mant eq "si"){
            $filename= $elemM->findnodes("image")->get_node(1)->textContent;
            $boolImg=0;
        }
        else{
            my $file= $elemM->findnodes("image")->get_node(1)->textContent;
            if($file ne "../immagini/noImg.jpg"){
                $file= substr $file, 3;
                $file= "../public_html/$file";
                unlink $file;
            }
        }
        if(!$boolImg){
            if($mant ne "si"){
                if($cat eq "gpc" || $cat eq "cpc"){
                    $filename="../immagini/games/pc/$filename";
                }
                if($cat eq "gxbox" || $cat eq "cxbox"){
                    $filename="../immagini/games/xbox/$filename";
                }
                if($cat eq "gps4" || $cat eq "cps4"){
                    $filename="../immagini/games/ps4/$filename";
                }
                if($cat eq "gnin" || $cat eq "cnin"){
                    $filename="../immagini/games/nintendo/$filename";
                }
            }
            $frammento= "<game>
                                <ID>".$id2."</ID>
                                <title>".$titolo."</title>
                                <category>".$cat."</category>
                                <description>".$desc."</description>
                                <image>".$filename."</image>
                                <date>".$date."</date>
                                <price>".$prez."</price>
            </game>";
        }
        else{
            $frammento= "<game>
                                <ID>".$id2."</ID>
                                <title>".$titolo."</title>
                                <category>".$cat."</category>
                                <description>".$desc."</description>
                                <image>".$noImg."</image>
                                <date>".$date."</date>
                                <price>".$prez."</price>
            </game>";
        }


        my $parent= $elemM->parentNode;
        $parent->removeChild($elemM);

        my $nodo= $parser->parse_balanced_chunk($frammento, 'UTF-8') || die("fail frammento");
        my $padre= $root;

        $padre->appendChild($nodo) || die("fail append");
        open(OUT, ">$fileXML");
        print OUT $doc->toString;
        close (OUT);

        $session->clear(["~logged-in", "idg"]);
        &printHeader("Caricamento Gioco/Console");
        print '<h3>CARICAMENTO AVVENUTO</h3>
                <a href="giochi.cgi?id='.$id2.'&amp;ty='.$cat.'">';
        if($cat eq "gpc" || $cat eq "gxbox" || $cat eq "gps4" || $cat eq "gnin"){
            print'Vai alla pagina del gioco</a>';
        }
        if($cat eq "cpc"){
            print'Vai alla pagina dell\'accessorio</a>';
        }
        if($cat eq "cxbox" || $cat eq "cps4" || $cat eq "cnin"){
            print'Vai alla pagina della console</a>';
        }
        &printFooter;
    }
}
else{
    &printHeader("ERRORE Gioco/Console");
    print '<h3 class="errori">ERRORE</h3>';
    if($stitolo eq ""){
        print'<h3 class="errori">Il titolo non pu&ograve; essere vuoto!</h3>';
    }
    if($sprez eq "" || !($sprez=~m /^([0-9]+.[0-9]{1,}$)/)){
        print' <h3 class="errori">Il prezzo non pu&ograve; essere vuoto e deve essere in questo formato: nnnn.nn dove n &egrave; un numero tra 0 e 9</h3>';
    }
    if($sdesc eq ""){
        print'<h3 class="errori">La descrizione non pu&ograve; essere vuota!</h3>';
    }
    if(!$idg){
        print'<a id="err" href="addGame.cgi?id='.$id2.'&amp;ty='.$cat.'">Torna indietro</a>';
    }
    else{
        print'<a id="err" href="addGame.cgi">Torna indietro</a>';
    }
    $session->clear(["~logged-in", "idg"]);

    &printFooter;
}
exit;
