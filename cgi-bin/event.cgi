#!/usr/bin/perl
use CGI;
use CGI::Session();
use XML::LibXML;
use HTML::Entities;
use File::Basename;
use CGI::Carp qw(fatalsToBrowser);
require 'utility.cgi';
require 'event_utility.cgi';
my $page=new CGI;
#recupero dati
$session= CGI::Session->load() or die "sessione non trovata";

my $titolo= $page->param('title');
utf8::encode($titolo);
my $mant= $page->param('mant'); #SERVE PER VEDERE SE VOGLIO MANTERE L'IMMAGINE O NO
my $filename= $page->param('image');
my $noImg="../immagini/noImg.jpg";
my $boolImg=0; #0= c'e immagine valida 1=immagine non valida
if ($filename eq ""){#USARE UN'ALTRO NOME AL POSTO DI FILENAME PER METTERE NOIMG
    $boolImg=1;

}
my $id2= $session->param('ide');
my $idg=0;
if(!$id2){
    $idg=1;
}
my $sizef= -s $filename;
my $extension3= substr $filename, -3;
if($mant ne "si" && ($sizef > 3072000 || ($extension3 && $extension3 ne "jpg" && $extension3 ne "png" && $extension3 ne "bmp"))){ #controllo per dimensione file ed estensione
    &printHeader("ERRORE Evento");
    print '<h3 class="errori">ERRORE</h3>';
    print '<h3 class="errori">formato non supportato o file troppo grande!!</h3>';
    if(!$idg){
        print'<a id="err" href="addEvent.cgi?id='.$id2.'">Torna indietro</a>';
    }
    else{
        print'<a id="err" href="addEvent.cgi">Torna indietro</a>';
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
my $desc= $page->param('desc');
utf8::encode($desc);

my $stitolo= $titolo;
$stitolo=~s/ //g;
$titolo=~s/&/&amp;/g;
$titolo=~s/>/&gt;/g;
$titolo=~s/</&lt;/g;

my $sdesc= $desc;
$desc=~s/&/&amp;/g;
$desc=~s/>/&gt;/g;
$desc=~s/</&lt;/g;


if(($stitolo ne "") && ($sdesc ne "")){
    if($mant ne "si" && $boolImg==0){
        $CGI::POST_MAX= 1024*3000;
        my $safe_filename_characters = "a-zA-Z0-9_.-";
        my $up_dir="../public_html/immagini/events";
        if($filename ne ""){
            my ($name, $path, $extension)= fileparse($filename, '.*');

            $filename= $name.$extension;
            $filename=~tr/ /_/;
            $filename=~s/[^$safe_filename_characters]//g;

            if ( $filename =~/^([$safe_filename_characters]+)$/ ){
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
   my $fileXML="../data/events.xml";

   my $parser= XML::LibXML->new();
   my $doc= $parser->parse_file($fileXML) || die("fail parser");
   my $root= $doc->getDocumentElement || die("fail radice");

   my @events= $root->getElementsByTagName("event");
   if(!$id2){
       my $idMax=0;
       foreach $elemento (@events){
           my $idCurr= $elemento->findnodes("ID")->get_node(1)->textContent;
           if($idCurr > $idMax){
               $idMax= $elemento->findnodes("ID")->get_node(1)->textContent;
           }
       }

       $newID= $idMax+1;
       my $frammento="";
       if($boolImg == 0){
           $filename= "../immagini/events/$filename";
           $frammento= "<event>
                            <ID>".$newID."</ID>
   		                    <title>".$titolo."</title>
                            <description>".$desc."</description>
   		                    <image>".$filename."</image>
   		                    <date>".$date."</date>
   	        </event>";
        }
        else{
            $frammento= "<event>
                            <ID>".$newID."</ID>
    		                <title>".$titolo."</title>
                            <description>".$desc."</description>
    		                <image>".$noImg."</image>
    		                <date>".$date."</date>
    	    </event>";
        }


       my $nodo= $parser->parse_balanced_chunk($frammento, 'UTF-8') || die("fail frammento");
       my $padre= $root;
       $padre->appendChild($nodo) || die("fail append");
       open(OUT, ">$fileXML");
       print OUT $doc->toString;
       close (OUT);
       &printHeader("Caricamento Evento");
       print '<h3>CARICAMENTO AVVENUTO</h3>
       <a href="eventi.cgi?id='.$newID.'">Vai alla pagina dell\'evento</a>';
       &printFooter;
    }
    else{
        my $elemM= $doc->findnodes("//event[ID=$id2]")->get_node(1);
        my $commentM= $elemM->findnodes("comments")->get_node(1);
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
                $filename= "../immagini/events/$filename";
            }
            $frammento= "<event>
                                <ID>".$id2."</ID>
                                <title>".$titolo."</title>
                                <description>".$desc."</description>
                                <image>".$filename."</image>
                                <date>".$date."</date>
                                ".$commentM."
                        </event>";

        }
        else{
            $frammento= "<event>
                                <ID>".$id2."</ID>
                                <title>".$titolo."</title>
                                <description>".$desc."</description>
                                <image>".$noImg."</image>
                                <date>".$date."</date>
                                ".$commentM."
                        </event>";
        }
        my $parent= $elemM->parentNode;
        $parent->removeChild($elemM);

        my $nodo= $parser->parse_balanced_chunk($frammento, 'UTF-8') || die("fail frammento");
        my $padre= $root;

        $padre->appendChild($nodo) || die("fail append");
        open(OUT, ">$fileXML");
        print OUT $doc->toString;
        close (OUT);

        $session->clear(["~logged-in", "ide"]);
        &printHeader("Caricamento Evento");
        print '<h3>CARICAMENTO AVVENUTO</h3>
        <a href="eventi.cgi?id='.$id2.'">Vai alla pagina dell\'evento</a>';
        &printFooter;
    }
}
else{
    &printHeader("ERRORE Evento");
    $session->clear(["~logged-in", "ide"]);
    print '<h3 class="errori">ERRORE</h3>';
    if($stitolo eq ""){
            print'<h3 class="errori">Il titolo non pu&ograve; essere vuoto!</h3>';
    }
    if($sdesc eq ""){
        print'<h3 class="errori">La descrizione non pu&ograve; essere vuota!</h3>';
    }
    if($idg){
        print'<a id="err" href="addEvent.cgi?id='.$id2.'">Torna indietro</a>';
    }
    else{
        print'<a id="err" href="addEvent.cgi">Torna indietro</a>';
    }
    $session->clear(["~logged-in", "ide"]);
    &printFooter;
}
exit;
