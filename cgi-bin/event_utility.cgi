#!/usr/bin/perl
use CGI; # importa la libreria CGI
use CGI::Session();
use HTML::Entities;
use CGI::Carp qw(fatalsToBrowser);
use Switch;
use XML::LibXML;
use POSIX qw(strftime);
use DateTime;

sub printFormComm{
    $idComm= shift; #oppure usare $page->param("id")
    $tab= shift;
    $session->param("idComm", $idComm);
    print'<div>
                <form action="addComment.cgi" method="post">
                    <fieldset>
                        <legend>Inserisci un nuovo commento</legend>
                        <label>Testo:<br/>
                        <textarea tabindex="'.$tab.'" rows="15" cols="50" name="testoC" ></textarea></label>';
                        $tab++;
                        print'<br/><input tabindex="'.$tab.'" type="submit" value="Inserisci" />
                        </fieldset>
                </form>
    </div>';
}

sub printContentE{
    my $tab=26;
    my $datestring2= strftime "%H:%M, %F", localtime;
    my $datestring= strftime "%d-%m-%Y", localtime;
    print '<h2>data di oggi: '.$datestring.'</h2>';
    my $page= new CGI;
    print '<h2>Eventi Futuri:</h2>';
    my $fileXML="../data/events.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @dates= $root->getElementsByTagName("date");
    #@dates= sort { $a cmp $b} @dates; <--SORTING PER DATE FORMAT YYYY-MM-DD
    @dates= sort { join('', (split '-', $a)[2,1,0]) cmp join('', (split '-', $b)[2,1,0]) } @dates;
    foreach $elem1 (@dates){
        my $elem= $elem1->parentNode;
        my $date= $elem->findnodes("date")->get_node(1)->textContent;
        $datestring= join('', (split '-', $datestring)[2,1,0]);
        my $date2= join('', (split '-', $date)[2,1,0]);
        if($date2 >= $datestring){
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $tit= $elem->findnodes("title")->get_node(1)->toString();
            utf8::decode($tit);
            $tit= substr $tit, 7, -8;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            my $desc= $elem->findnodes("description")->get_node(1)->textContent;
            utf8::decode($desc);

            my $descP= substr $desc, 0, 120;
            print '<div class="event">
                        <div class="eventcontent">
                            <a tabindex="'.$tab.'" class="eventlink" href="eventi.cgi?id='.$id.'" title="link evento'.$id.'">
                            link evento'.$id.'</a>
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
                            $tab++;
                            print '<div class="controlPanel">
                                <a tabindex="'.$tab.'" href="addEvent.cgi?id='.$id.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                $tab++;
                                print'<a tabindex="'.$tab.'" href="removeEvent.cgi?id='.$id.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                            </div>';
                        }
            print'</div>';
        }
    }
    $tab++;
    print '<br class="clearFloat" /><h2>Eventi Passati:</h2>';
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    #@dates= sort {$b cmp $a} @dates; <--SORTING PER DATE FORMAT YYYY-MM-DD
    foreach $elem1 (@dates){
        $elem= $elem1->parentNode;
        my $date= $elem->findnodes("date")->get_node(1)->textContent;
        $datestring= join('', (split '-', $datestring)[2,1,0]);
        my $date2= join('', (split '-', $date)[2,1,0]);
        if($date2 < $datestring){
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $tit= $elem->findnodes("title")->get_node(1)->toString();
            utf8::decode($tit);
            $tit= substr $tit, 7, -8;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            my $desc= $elem->findnodes("description")->get_node(1)->textContent;
            utf8::decode($desc);

            my $descP= substr $desc, 0, 120;
            print '<div class="event">
                        <div class="eventcontent">
                            <a tabindex="'.$tab.'" class="eventlink" href="eventi.cgi?id='.$id.'">link evento'.$id.'</a>
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
                            $tab++;
                            print '<div class="controlPanel">
                                <a tabindex="'.$tab.'" href="addEvent.cgi?id='.$id.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                $tab++;
                                print'<a tabindex="'.$tab.'" href="removeEvent.cgi?id='.$id.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                            </div>';
                        }
            print'</div>';
        }
    }
}

sub printFormE{
    my $page= new CGI;
    my $id= $page->param('id');
    if($id){
        $session->param("ide", $id);
        my $fileXML="../data/events.xml";
        my $parser= XML::LibXML->new();
        my $doc= $parser->parse_file($fileXML) || die("fail parser");
        my $root= $doc->getDocumentElement || die("fail radice");

        my @event= $root->getElementsByTagName("event");

        foreach $elem (@event){
            my $idCurr= $elem->findnodes("ID")->get_node(1)->textContent;
            if($idCurr == $id){
                my $tit= $elem->findnodes("title")->get_node(1)->textContent;
                $tit=~s/&+/&amp/;
                utf8::decode($tit);
                my $desc= $elem->findnodes("description")->get_node(1)->textContent;
                #my $desc= $elem->findnodes("description")->get_node(1)->textContent;
                utf8::decode($desc);
                #$desc=~s/\n//g;

                #$desc= substr $desc, 13, -14;
                my $date= $elem->findnodes("date")->get_node(1)->textContent;
                print '<form action="event.cgi" method="post" enctype="multipart/form-data">
                            <fieldset>
                                <legend>Inserisci i dati del nuovo evento</legend>
                                <label>Titolo <input tabindex="26" type="text" name="title" value="'.$tit.'" /></label><br />
                                <label for="mantieniImg">Mantenere immagine corrente <input tabindex="27" type="checkbox" id="mantieniImg" value="si" name="mant" checked="checked"/></label><br/>
                                <label id="lImg">Immagine (dimensione massima 3MB e formati accettati: jpg, png e bmp)
                                    <input tabindex="28" type="file" id="fImg" name="image" accept="image/*" /><span id="immagine"></span></label>

                                <br/><label>Data ';
                                my ($dayM, $monthM, $yearM)= split /-/, $date;
                                print '<select tabindex="29" name="day">';
                                foreach($i=1; $i<=31; $i++){
                                    if($i==$dayM){
                                        print '<option  value="'.$i.'" selected="selected">'.$i.'</option>';
                                    }
                                    else{
                                        print '<option  value="'.$i.'">'.$i.'</option>';
                                    }
                                }
                                print '</select></label>
                                <label for="month">
                                <select tabindex="30" id="month" name="month">';
                                foreach($i=1; $i<=12; $i++){
                                    if($i==$monthM){
                                        print '<option  value="'.$i.'" selected="selected">'.$i.'</option>';
                                    }
                                    else{
                                        print '<option  value="'.$i.'">'.$i.'</option>';
                                    }
                                }
                                print '</select></label>
                                <label for="year">
                                <select tabindex="31" id="year" name="year">';
                                foreach($i=1980; $i<=2020; $i++){
                                    if($i==$yearM){
                                        print '<option  value="'.$i.'" selected="selected">'.$i.'</option>';
                                    }
                                    else{
                                        print '<option  value="'.$i.'">'.$i.'</option>';
                                    }
                                }
                                print '</select></label><br />

                                <label>Descrizione <br /><textarea tabindex="32" rows="15" cols="50" name="desc" >'.$desc.'</textarea></label><br />
                                <input tabindex="33" id="conf" type="submit" value="Inserisci" />
                                <input tabindex="34" type="reset" value="Reimposta" />
                        </fieldset>
                </form>';
            }
        }
    }
    else{
        print'<form id="formImg" action="event.cgi" method="post" enctype="multipart/form-data">
                    <fieldset>
                        <legend>Inserisci i dati del nuovo evento</legend>
                        <label>Titolo <input tabindex="26" type="text" name="title" /></label><br />
                        <label>Immagine (dimensione massima 3MB e formati accettati: jpg, png e bmp) <input tabindex="27" type="file" id="fImg" name="image" accept="image/*" /><span id="immagine"></span></label><br />
                        <label>Data <select tabindex="28" name="day">';
                        foreach($i=1; $i<=31; $i++){
                            print '<option  value="'.$i.'">'.$i.'</option>';
                        }
                        print '</select></label>
                        <label for="month">
                        <select tabindex="29" id="month" name="month">';
                        foreach($i=1; $i<=12; $i++){
                            print '<option  value="'.$i.'">'.$i.'</option>';
                        }
                        print '</select></label>
                        <label for="year">
                        <select tabindex="30" id="year" name="year">';
                        foreach($i=1980; $i<=2020; $i++){
                            print '<option  value="'.$i.'">'.$i.'</option>';
                        }
                        print '</select></label><br />

                        <label>Descrizione<br /><textarea tabindex="31" rows="15" cols="50" name="desc" ></textarea></label><br />
                        <input tabindex="32" type="submit" value="Inserisci" />
                        <input tabindex="33" type="reset" value="Reimposta" />
                    </fieldset>
        </form>';
    }
}
1;
