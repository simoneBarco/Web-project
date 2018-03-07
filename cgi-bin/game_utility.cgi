#!/usr/bin/perl
use CGI; # importa la libreria CGI
use CGI::Session();
use HTML::Entities;
use CGI::Carp qw(fatalsToBrowser);
use Switch;
use XML::LibXML;

sub printContentG{
    my $page=new CGI;
    my $ty= $page->param('ty');
    if($ty eq 'gpc'){
        &printHeader("Lista giochi PC");
        &printLista($ty);
    }
    elsif($ty eq 'gxbox'){
        &printHeader("Lista giochi XBox");
        &printLista($ty);
    }
    elsif($ty eq 'gps4'){
        &printHeader("Lista giochi PS4");
        &printLista($ty);
    }
    elsif($ty eq 'gnin'){
        &printHeader("Lista giochi Nintendo");
        &printLista($ty);
    }
    elsif($ty eq 'cpc'){
        &printHeader("Lista Accessori PC");
        &printLista($ty);
    }
    elsif($ty eq 'cxbox'){
        &printHeader("Lista console XBox");
        &printLista($ty);
    }
    elsif($ty eq 'cps4'){
        &printHeader("Lista console PS4");
        &printLista($ty);
    }
    elsif($ty eq 'cnin'){
        &printHeader("Lista console Nintendo");
        &printLista($ty);
    }
    else{
        &printHeader("ERRORE");
        print'<h3 class="errori">Nessuna categoria selezionata!</h3>
                <h3 class="errori">Scegline una dal menu!</h3>';
                &printFooter;
                exit;
    }

}

sub printLista{
    my $ty= shift;
    my $fileXML="";
    my $cons= 0;
    if($ty eq 'gpc' || $ty eq 'cpc'){
        if($ty eq 'cpc'){
            $cons= 1;
        }
        $fileXML="../data/pc_games.xml";
    }
    if($ty eq 'gxbox' || $ty eq 'cxbox'){
        if($ty eq 'cxbox'){
            $cons= 1;
        }
        $fileXML="../data/xbox_games.xml";
    }
    if($ty eq 'gps4' || $ty eq 'cps4'){
        if($ty eq 'cps4'){
            $cons= 1;
        }
        $fileXML="../data/ps4_games.xml";
    }
    if($ty eq 'gnin' || $ty eq 'cnin'){
        if($ty eq 'cnin'){
            $cons= 1;
        }
        $fileXML="../data/nintendo_games.xml";
    }

    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");

    my @games= $root->getElementsByTagName("game");
    if($cons == 0){
        my $tab=26;
        foreach $elem (@games){
            my $cat= $elem->findnodes("category")->get_node(1)->textContent;
            if($cat ne 'cpc' && $cat ne 'cxbox' && $cat ne 'cps4' && $cat ne 'cnin' ){
                my $id= $elem->findnodes("ID")->get_node(1)->textContent;
                my $tit= $elem->findnodes("title")->get_node(1)->toString();
                utf8::decode($tit);
                $tit= substr $tit, 7, -8;
                my $prez= $elem->findnodes("price")->get_node(1)->textContent;
                my $image= $elem->findnodes("image")->get_node(1)->textContent;
                print '<div class="games">
                            <div class="picture">
                                <a tabindex="'.$tab.'" href="giochi.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="'.$image.'" alt="'.$tit.'"/></a>
                                <div class="descrizione">
                                    <div class="info">'.$tit.'</div>
                                    <div class="prezzo">'.$prez.'&euro;</div>';
                                    my $tmpUser=&getSession();
                                    if($tmpUser eq 'admin@mail.com'){
                                        $tab++;
                                        print '<div class="controlPanel">
                                            <a tabindex="'.$tab.'" href="addGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                            $tab++;
                                            print'<a tabindex="'.$tab.'" href="removeGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                                        </div>';
                                    }
                                print'</div>
                            </div>
                </div>';
            }
        }
    }
    if($cons==1){
        foreach $elem (@games){
            my $cat= $elem->findnodes("category")->get_node(1)->textContent;
            if($cat eq 'cpc' || $cat eq 'cxbox' || $cat eq 'cps4' || $cat eq 'cnin'){
                my $id= $elem->findnodes("ID")->get_node(1)->textContent;
                my $tit= $elem->findnodes("title")->get_node(1)->textContent;
                utf8::decode($tit);
                my $prez= $elem->findnodes("price")->get_node(1)->textContent;
                my $image= $elem->findnodes("image")->get_node(1)->textContent;
                $tab++;
                print '<div class="games">
                            <div class="picture">
                                <a tabindex="'.$tab.'" href="giochi.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="'.$image.'" alt="'.$tit.'"/></a>
                                <div class="descrizione">
                                <div class="info">'.$tit.'</div>
                                <div class="prezzo">'.$prez.'&euro;</div>';
                                my $tmpUser=&getSession();
                                if($tmpUser eq 'admin@mail.com'){
                                    $tab++;
                                    print '<div class="controlPanel">
                                        <a tabindex="'.$tab.'" href="addGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/modifica.png" alt="modifica"/></a>';
                                        $tab++;
                                        print'<a tabindex="'.$tab.'" href="removeGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                                    </div>';
                                }
                            print'</div>
                        </div>
                </div>';
            }
        }
    }
}
sub printFormG{
    #my $session= new CGI::Session->load() or die ("sessione non trovata");
    my $page= new CGI;
    my $id= $page->param('id');
    my $ty= $page->param('ty');
    if($id){
        $session->param("idg", $id);
        $session->param("tyg", $ty);
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
        if($ty eq ""){
            print 'nessuna categoria selezionata';
            exit;
        }
        my $parser= XML::LibXML->new();
        my $doc= $parser->parse_file($fileXML) || die("fail parser");
        my $root= $doc->getDocumentElement || die("fail radice");

        my @games= $root->getElementsByTagName("game");

        foreach $elem (@games){
            my $idCurr= $elem->findnodes("ID")->get_node(1)->textContent;
            if($idCurr == $id){
                my $tit= $elem->findnodes("title")->get_node(1)->textContent;
                utf8::decode($tit);
                my $prez= $elem->findnodes("price")->get_node(1)->textContent;
                my $image= $elem->findnodes("image")->get_node(1)->textContent;
                my $desc= $elem->find("description")->get_node(1)->textContent;
                utf8::decode($desc);
                #$desc=~s/\n/<br\/>/g;
                #$desc= substr $desc, 13, -14;
                $desc=~s/\n//g;
                my $date= $elem->findnodes("date")->get_node(1)->textContent;
                print '<form action="games.cgi" method="post" enctype="multipart/form-data">
                            <fieldset>
                                <legend>Modifica i dati gioco</legend>
                                <label>Titolo <input tabindex="26" type="text" name="title" value="'.$tit.'" /></label><br />
                                <label>Categoria
                                <select tabindex="27" name="cat">';
                                    switch($ty){
                                        case 'gpc'{
                                            print '<option value="gpc" selected="selected">Giochi -&gt; PC</option>
                                            <option value="gxbox">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'gxbox'{
                                            print '<option value="gpc" >Giochi -&gt; PC</option>
                                            <option value="gxbox" selected="selected">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'gps4'{
                                            print '<option value="gpc" >Giochi -&gt; PC</option>
                                            <option value="gxbox" >Giochi -&gt; XBox</option>
                                            <option value="gps4" selected="selected">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'gnin'{
                                            print '<option value="gpc" >Giochi -&gt; PC</option>
                                            <option value="gxbox" >Giochi -&gt; XBox</option>
                                            <option value="gps4" >Giochi -&gt; PS4</option>
                                            <option value="gnin" selected="selected">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'cpc'{
                                            print '<option value="gpc">Giochi -&gt; PC</option>
                                            <option value="gxbox">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc" selected="selected">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'cxbox'{
                                            print '<option value="gpc">Giochi -&gt; PC</option>
                                            <option value="gxbox">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox" selected="selected">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'cps4'{
                                            print '<option value="gpc">Giochi -&gt; PC</option>
                                            <option value="gxbox">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4" selected="selected">Console -&gt; PS4</option>
                                            <option value="cnin">Console -&gt; Nintendo</option>';
                                        }
                                        case 'cnin'{
                                            print '<option value="gpc">Giochi -&gt; PC</option>
                                            <option value="gxbox">Giochi -&gt; XBox</option>
                                            <option value="gps4">Giochi -&gt; PS4</option>
                                            <option value="gnin">Giochi -&gt; Nintendo</option>
                                            <option value="cpc">Console -&gt; Accessori PC</option>
                                            <option value="cxbox">Console -&gt; XBox</option>
                                            <option value="cps4">Console -&gt; PS4</option>
                                            <option value="cnin" selected="selected">Console -&gt; Nintendo</option>';
                                        }
                                    }
                                print'</select></label><br />
                                <label for="mantieniImg">Mantenere immagine corrente <input tabindex="28" type="checkbox" value="si" id="mantieniImg" name="mant" checked="checked"/></label><br/>
                                <label id="lImg">Immagine (dimensione massima 3MB e formati accettati: jpg, png e bmp)
                                    <input tabindex="29" type="file" id="fImg" name="image" accept="image/*" /><span id="immagine"></span>
                                </label>
                                <br/><label>Data ';
                                my ($dayM, $monthM, $yearM)= split /-/, $date;
                                print '<select tabindex="30" name="day">';
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
                                <select tabindex="31" id="month" name="month">';
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
                                <select tabindex="32" id="year" name="year">';
                                foreach($i=1980; $i<=2020; $i++){
                                    if($i==$yearM){
                                        print '<option  value="'.$i.'" selected="selected">'.$i.'</option>';
                                    }
                                    else{
                                        print '<option  value="'.$i.'">'.$i.'</option>';
                                    }
                                }
                                print '</select></label><br />
                                <label>Prezzo <input tabindex="33" type="text" name="price" value="'.$prez.'"/></label><br />
                                <label>Descrizione <br /><textarea tabindex="34" rows="15" cols="50" name="desc">'.$desc.'</textarea></label><br />
                                <input tabindex="35" id="conf" type="submit" value="Inserisci" />
                                <input tabindex="36" type="reset" value="Reimposta" />
                            </fieldset>
                    </form>';
            }
        }
   }
   else{
        print'<form action="games.cgi" method="post" enctype="multipart/form-data">
                    <fieldset>
                        <legend>Inserisci i dati del nuovo gioco</legend>
                        <label>Titolo <input tabindex="26" type="text" name="title" /></label><br />
                        <label>Categoria
                        <select tabindex="27" name="cat">
                            <option value="gpc">Giochi -&gt; PC</option>
                            <option value="gxbox">Giochi -&gt; XBox</option>
                            <option value="gps4">Giochi -&gt; PS4</option>
                            <option value="gnin">Giochi -&gt; Nintendo</option>
                            <option value="cpc">Console -&gt; Accessori PC</option>
                            <option value="cxbox">Console -&gt; XBox</option>
                            <option value="cps4">Console -&gt; PS4</option>
                            <option value="cnin">Console -&gt; Nintendo</option>
                        </select></label><br />
                        <label>Immagine (dimensione massima 3MB e formati accettati: jpg, png e bmp) <input tabindex="28" type="file" id="fImg" name="image" accept="image/*" /><span id="immagine"></span></label><br />
                        <label>Data
                        <select tabindex="29" name="day">';
                            foreach($i=1; $i<=31; $i++){
                                print '<option  value="'.$i.'">'.$i.'</option>';
                            }
                            print '</select></label>
                        <label for="month">
                        <select tabindex="30" id="month" name="month">';
                            foreach($i=1; $i<=12; $i++){
                                print '<option  value="'.$i.'">'.$i.'</option>';
                            }
                            print '</select></label>
                        <label for="year">
                        <select tabindex="31" id="year" name="year">';
                            foreach($i=1980; $i<=2020; $i++){
                                print '<option  value="'.$i.'">'.$i.'</option>';
                            }
                        print '</select></label><br />
                        <label>Prezzo <input tabindex="32" type="text" name="price" /></label><br />
                        <label>Descrizione <br /><textarea tabindex="33" rows="15" cols="50" name="desc"></textarea></label><br />
                        <input tabindex="34" type="submit" value="Inserisci" />
                        <input tabindex="35" type="reset" value="Reimposta" />
                    </fieldset>
         </form>';
    }
}
1;
