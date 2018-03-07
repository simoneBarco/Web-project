#!/usr/bin/perl
use CGI;
use XML::LibXML;
require "utility.cgi";
require "game_utility.cgi";
my $page=new CGI;

my $id=$page->param('id');
my $ty=$page->param('ty');
if($id){
    my $cat="";
    my $fileXML="";
    if($ty eq 'gpc'){
        $fileXML="../data/pc_games.xml";
        $cat="PC";
    }
    if($ty eq 'gxbox'){
        $fileXML="../data/xbox_games.xml";
        $cat="XBox";
    }
    if($ty eq 'gps4'){
        $fileXML="../data/ps4_games.xml";
        $cat="PS4";
    }
    if($ty eq 'gnin'){
        $fileXML="../data/nintendo_games.xml";
        $cat="Nintendo";
    }
    if($ty eq 'cpc'){
        $fileXML="../data/pc_games.xml";
        $cat="Accessori PC";
    }
    if($ty eq 'cxbox'){
        $fileXML="../data/xbox_games.xml";
        $cat="Console XBox";
    }
    if($ty eq 'cps4'){
        $fileXML="../data/ps4_games.xml";
        $cat="Console PS4";
    }
    if($ty eq 'cnin'){
        $fileXML="../data/nintendo_games.xml";
        $cat="Console Nintendo";
    }

    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");

    my @games= $root->getElementsByTagName("game");

    foreach $elem (@games){
        my $idCurr= $elem->findnodes("ID")->get_node(1)->textContent;
        if($idCurr == $id){

            my $tit= $elem->findnodes("title")->get_node(1)->toString();
            utf8::decode($tit);
            $tit= substr $tit, 7, -8;
            my $date= $elem->findnodes("date")->get_node(1)->textContent;
            my $prez= $elem->findnodes("price")->get_node(1)->textContent;
            #my $desc= $elem->findnodes("description")->get_node(1)->toString();
            my $desc= $elem->findnodes("description")->get_node(1)->textContent;
            utf8::decode($desc);
            $desc=~s/\n/<br\/>/g;
            &printHeader("$tit $cat");
            #$desc= substr $desc, 13, -14;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            print'<div class="gameDescription">
                        <img src="'.$image.'" alt="'.$tit.'" />
                        <div>
                            <h1>Titolo: '.$tit.' </h1>
                            <h2>Prezzo: '.$prez.'&euro;</h2>
                            <h3>Data uscita: '.$date.'</h3>
                            <h3>Descrizione:</h3>
                            <p>'.$desc.'</p>
                        </div>
            </div>';
            my $tmpUser=&getSession();
            if($tmpUser eq 'admin@mail.com'){
                print '<div class="controlPanel">
                    <a href="addGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/modifica.png" alt="modifica"/></a>
                    <a href="removeGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                </div>';
            }
        }
    }
    &printFooter;
}
else{
    &printContentG;
    &printFooter;
}
exit;
