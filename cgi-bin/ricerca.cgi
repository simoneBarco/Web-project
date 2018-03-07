#!/usr/bin/perl
use CGI;
use XML::LibXML;
require "utility.cgi";

my $page= new CGI;
my $search= $page->param("search");
utf8::encode($search);

my $ssearch= $search;
$ssearch=~s/ //g;
$ssearch=lc $ssearch;
&printHeader("Risultati per \'$search\'");

my $trovato= 0;
my $parser= XML::LibXML->new();
for(my $i=0; $i<4; $i++){
    my $fileXML= "";
    my $cat= "";
    if($i==0){
        $fileXML="../data/pc_games.xml";
        $cat="PC"
    }
    if ($i==1){
        $fileXML="../data/xbox_games.xml";
        $cat="XBox"
    }
    if ($i==2){
        $fileXML="../data/ps4_games.xml";
        $cat="PS4"
    }
    if ($i==3){
        $fileXML="../data/nintendo_games.xml";
        $cat="Nintendo"
    }
    my $doc= $parser->parse_file($fileXML) || die("fail parser");
    my $root= $doc->getDocumentElement || die("fail radice");
    my @games= $root->getElementsByTagName("game");


    foreach $elem(@games){
        my $tit= $elem->findnodes("title")->get_node(0)->textContent;
        utf8::decode($tit);
        my $stit= $tit;
        $stit=~s/ //g;
        $stit= lc $stit;
        if($stit eq $ssearch){
            #print "<h3>Giochi $cat:</h3>";
            $trovato=1;
            my $id= $elem->findnodes("ID")->get_node(1)->textContent;
            my $date= $elem->findnodes("date")->get_node(1)->textContent;
            my $ty= $elem->findnodes("category")->get_node(1)->textContent;
            my $prez= $elem->findnodes("price")->get_node(1)->textContent;
            my $desc= $elem->findnodes("description")->get_node(1)->toString();
            utf8::decode($desc);
            #&printHeader("$tit $cat");
            $desc= substr $desc, 13, -14;
            my $image= $elem->findnodes("image")->get_node(1)->textContent;
            print '<div class="games">
                        <h3>'.$cat.'</h3>
                        <div class="picture">
                            <a href="giochi.cgi?id='.$id.'&amp;ty='.$ty.'" tabindex="41"><img src="'.$image.'" alt="immagine del gioco '.$tit.'"/></a>
                            <div class="descrizione">
                                <div class="info">'.$tit.'</div>
                                <div class="prezzo">'.$prez.'</div>';
                                my $tmpUser=&getSession();
                                if($tmpUser eq 'admin@mail.com'){
                                    print '<div class="controlPanel">
                                        <a href="addGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/modifica.png" alt="modifica"/></a>
                                        <a href="removeGame.cgi?id='.$id.'&amp;ty='.$ty.'"><img src="../immagini/elimina.png" alt="elimina"/></a>
                                    </div>';
                                }
                            print'</div>
                        </div>
            </div>';
        }
    }

}
if($trovato == 0){
    print "<h3 class=\"errori\">Nessun risultato trovato!</h3>";
}


&printFooter;
