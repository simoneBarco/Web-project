#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
my $page=new CGI;
my $cg= $page->param("cg");
my $tab=26;
if($cg == 1){
    &printHeader("Giochi");
    my $fileXML="../data/pc_games.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    my $i= 0;
    print '<h2>Ultimi giochi PC usciti</h2>';
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "gpc"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultimi giochi XBox usciti</h2>';
    $fileXML="../data/xbox_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "gxbox"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultimi giochi PS4 usciti</h2>';
    $fileXML="../data/ps4_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "gps4"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultimi giochi Nintendo usciti</h2>';
    $fileXML="../data/nintendo_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "gnin"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
else{
    &printHeader("Console");
    my $fileXML="../data/pc_games.xml";
    my $parser= XML::LibXML->new();
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    my $i= 0;
    $tab++;
    print '<h2>Ultimi Accessori PC usciti</h2>';
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "cpc"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultime console XBox uscite</h2>';
    $fileXML="../data/xbox_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "cxbox"){
            $i++;
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
                               <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultime console PS4 uscite</h2>';
    $fileXML="../data/ps4_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "cps4"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
    $tab++;
    print '<br class="clearFloat" /><h2>Ultime console Nintendo uscite</h2>';
    $fileXML="../data/nintendo_games.xml";
    $doc= $parser->parse_file($fileXML) || die("fail parser");
    $root= $doc->getDocumentElement || die("fail radice");
    @dates= $root->getElementsByTagName("date");
    @dates= sort { join('', (split '-', $b)[2,1,0]) cmp join('', (split '-', $a)[2,1,0]) } @dates;
    $i= 0;
    foreach $elem1(@dates){
        if($i==3){
            last;
        }
        $elem= $elem1->parentNode;
        my $cat= $elem->findnodes("category")->get_node(1)->textContent;
        if($cat eq "cnin"){
            $i++;
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
                                <div class="prezzo">'.$prez.'</div>';
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
