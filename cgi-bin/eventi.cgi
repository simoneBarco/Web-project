#!/usr/bin/perl
use CGI;
use XML::LibXML;
require "utility.cgi";
require "event_utility.cgi";
#&printHeader("Lista Eventi");
my $page=new CGI;

my $id=$page->param('id');
if($id){
    #&printHeader("Evento $id");
    my $fileXML="../data/events.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");

    my @events= $root->getElementsByTagName("event");
    my $tab=26;
    foreach $elem(@events){
        my $idCurr= $elem->findnodes("ID")->get_node(1)->textContent;
        if($idCurr == $id){
            my $tit= $elem->findnodes("title")->get_node(1)->toString();
            utf8::decode($tit);
            $tit= substr $tit, 7, -8;
            my $date= $elem->findnodes("date")->get_node(1)->textContent;
            my $desc= $elem->findnodes("description")->get_node(1)->textContent;
            utf8::decode($desc);
            $desc=~s/\n/<br\/>/g;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            &printHeader("$tit Evento");
            print '<div class="eventImmage">
                        <img src="'.$image.'" alt="'.$tit.'" />
                        <div>
                            <h1>'.$tit.'</h1>
                            <h2>'.$date.'</h2>
                            <p>'.$desc.'</p>
                        </div>
            </div>';
            my $tmpUser=&getSession();
            if($tmpUser eq 'admin@mail.com'){
                print '<div class="controlPanel">
                            <a tabindex="'.$tab.'" href="addEvent.cgi?id='.$id.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                            $tab++;
                            print'<a tabindex="'.$tab.'" href="removeEvent.cgi?id='.$id.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                </div>';
            }
            #SISTEMARE LA SELEZIONE DEI COMMENTI
            my $comments= $elem->findnodes("comments")->get_node(1);
            #my @dates= $elem->findnodes("comment//dataEora");
            #@dates= sort { join('', (split '-', $a)[2,1,0]) cmp join('', (split '-', $b)[2,1,0]) } @dates;
            #print 'date='.@dates;
            if($comments){
                my @comment= $comments->findnodes("comment");
                my @dates= $elem->getElementsByTagName("dataEora");
                @dates= sort { join('', (split ',-:', $a)[2,1,0,3,4]) cmp join('', (split ',-:', $b)[2,1,0,3,4]) } @dates;
                foreach $elemD(@dates){
                    my $elemC= $elemD->parentNode;
                    my $nr= $elemC->findnodes("nr")->get_node(1)->textContent;
                    my $nick= $elemC->findnodes("nickname")->get_node(1)->textContent;
                    my $dataC= $elemC->findnodes("dataEora")->get_node(1)->textContent;
                    my $text= $elemC->findnodes("testo")->get_node(1)->toString;
                    utf8::decode($text);
                    $text= substr $text, 7, -8;
                    print'<div class="comments">
                                <div class="utente">
                                    <h1>#'.$nr.' '.$nick.'</h1>
                                    <h2>'.$dataC.'</h2>
                                </div>
                                <div>
                                    <p>'.$text.'</p>
                                </div>
                    </div>';
                    if(&getSession() eq 'admin@mail.com'){
                        $tab++;
                        print'<div class="controlPanel">
                                <a tabindex="'.$tab.'" href="removeComment.cgi?idEvent='.$id.'&amp;idComm='.$nr.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                        </div>';
                    }
                    #$nr= $nr+1;
                    #push @dates, $dataEora;
                }
            }
            else{
                print'<h3>NESSUN COMMENTO</h3>';
            }
            if(&getSession()){
                &printFormComm($idCurr, $tab);
            }
            else{
                print'<h3 class="errori">DEVI ESSERE LOGGATO PER POTER AGGIUNGERE UN COMMENTO</h3>';
            }
        }
      #inserire for per i COMMENTI
    }
    &printFooter;
}
else{
    &printHeader("Lista eventi");
    &printContentE;
    &printFooter;
}
exit;
