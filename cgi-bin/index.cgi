#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
use POSIX qw(strftime);
require "utility.cgi";
&printHeader("Home");

my $datestring= strftime "%d-%m-%Y", localtime;


print '<h2>data di oggi: '.$datestring.'</h2>
<h2>Prossimo evento</h2>';
my $fileXML="../data/events.xml";
my $parser= XML::LibXML->new();
my $doc= $parser->parse_file($fileXML) || die("fail parser");
my $root= $doc->getDocumentElement || die("fail radice");
my @dates= $root->getElementsByTagName("date");
#@dates= sort { $a cmp $b} @dates; <--SORTING PER DATE FORMAT YYYY-MM-DD
@dates= sort { join('', (split '-', $a)[2,1,0]) cmp join('', (split '-', $b)[2,1,0]) } @dates;
my $i2= 0;
foreach $elem1 (@dates){
    if($i2== 1){
        last;
    }
    else{
        $elem= $elem1->parentNode;
        my $date= $elem->findnodes("date")->get_node(1)->textContent;
        $datestring= join('', (split '-', $datestring)[2,1,0]);
        my $date2= join('', (split '-', $date)[2,1,0]);
        if($date2 >= $datestring){
            $i2=1;
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $tit= $elem->findnodes("title")->get_node(1)->textContent;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            my $desc= $elem->findnodes("description")->get_node(1)->textContent;
            my $descP= substr $desc, 0, 80;
            utf8::decode($descP);
            print '<div class="event"><!--Preview di un evento-->
                        <div class="eventcontent">
                            <a class="eventlink" tabindex="23" href="eventi.cgi?id='.$id.'"></a>
                            <div class="eventdescription">
                                <div>
                                    <h1>'.$tit.'</h1>'.
                                    $date.'
                                    <h2>'.$descP.'...</h2>
                                </div>
                                <img src="'.$image.'" alt="'.$tit.'" />
                            </div>
                        </div>';
                        my $tmpUser=&getSession();
                        if($tmpUser eq 'admin@mail.com'){
                            print '<div class="controlPanel">
                                        <a tabindex="24" href="addEvent.cgi?id='.$id.'"><img src="../immagini/modifica.png" alt="modifica"/></a>
                                        <a tabindex="25" href="removeEvent.cgi?id='.$id.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                            </div>';
                        }
            print'</div>';
        }
    }
}
print '<br class="clearFloat" />
<h2>Ultimi giochi usciti</h2>';
$fileXML="../data/pc_games.xml";
my $tab=26;
foreach(my $i=0;$i<4;$i++){
    if($i==4){
        last;
    }
    if($i==1){
        $fileXML="../data/xbox_games.xml";
    }
    if($i==2){
        $fileXML="../data/ps4_games.xml";
    }
    if($i==3){
        $fileXML="../data/nintendo_games.xml";
    }
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    my $i2=0;
    foreach $elem2(@dates){
        if($i2==1){
            last;
        }
        my $elem= $elem2->parentNode;
        my $date= $elem->findnodes("date")->get_node(1)->textContent;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat ne 'cpc' && $cat ne 'cxbox' && $cat ne 'cps4' && $cat ne 'cnin' ){
            $i2++;
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $tit= $elem->findnodes("title")->get_node(1)->toString();
            utf8::decode($tit);
            $tit= substr $tit, 7, -8;
            my $prez= $elem->findnodes("price")->get_node(1)->textContent;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            print '<div class="games">
                        <div class="picture">
                            <a tabindex="'.$tab.'" href="giochi.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="'.$image.'" alt="'.$tit.'"/></a>
                            <div class="descrizione">
                                <div class="info">'.$tit.'</div>
                                <div class="prezzo">'.$prez.'&euro;</div>';
                                my $tmpUser=&getSession();
                                if($tmpUser eq 'admin@mail.com'){
                                    $tab++;
                                    print '<div class="controlPanel">
                                                <a tabindex="'.$tab.'" href="addGame.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                                $tab++;
                                                print'<a tabindex="'.$tab.'" href="removeGame.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                                    </div>';
                                }
                            print'</div>
                        </div>
            </div>';
        }
    }
}
$tab++;
print '<br class="clearFloat" />
<h2>Ultime console uscite</h2>';
$fileXML="../data/pc_games.xml";
foreach(my $i=0;$i<4;$i++){
    if($i==4){
        last;
    }
    if($i==1){
        $fileXML="../data/xbox_games.xml";
    }
    if($i==2){
        $fileXML="../data/ps4_games.xml";
    }
    if($i==3){
        $fileXML="../data/nintendo_games.xml";
    }
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    my $i2= 0;
    foreach $elem2(@dates){
        if($i2==1){
            last;
        }
        my $elem= $elem2->parentNode;
        my $date= $elem->findnodes("date")->get_node(1)->textContent;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat ne 'gpc' && $cat ne 'gxbox' && $cat ne 'gps4' && $cat ne 'gnin' ){
            $i2++;
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $tit= $elem->findnodes("title")->get_node(1)->textContent;
            my $prez= $elem->findnodes("price")->get_node(1)->textContent;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            print '<div class="games">
                        <div class="picture">
                            <a tabindex="'.$tab.'" href="giochi.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="'.$image.'" alt="'.$tit.'"/></a>
                            <div class="descrizione">
                                <div class="info">'.$tit.'</div>
                                <div class="prezzo">'.$prez.'&euro;</div>';
                                my $tmpUser=&getSession();
                                if($tmpUser eq 'admin@mail.com'){
                                    $tab++;
                                    print '<div class="controlPanel">
                                        <a tabindex="'.$tab.'" href="addGame.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                        $tab++;
                                        print'<a tabindex="'.$tab.'" href="removeGame.cgi?id='.$id.'&amp;ty='.$cat.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                                    </div>';
                                }
                            print'</div>
                        </div>
            </div>';
        }
    }
}
&printFooter;
exit;
