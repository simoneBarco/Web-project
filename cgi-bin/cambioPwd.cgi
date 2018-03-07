#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
my $page= new CGI;
$session= CGI::Session->load() or die "sessione non trovata";

#controllare che non si inserisca la email a mano e quindi sarebbe possibile cambiare la password di tutti
my $tmpUserM1= $page->param('usr');
my $tmpUserM2= $session->param('tmpUserM');
my $usrCurr= getSession();
if(!$usrCurr){
    &printHeader("ERRORE autenticazione");
    print'<h3 class="errori">ERRORE DEVI ESSERE LOGGATO PER POTER CAMBIARE LA TUA <span xml:lang=\'en\'>PASSWORD</span>!!!</h3>';
    &printFooter;
    exit;
}
my $ok= $page->param('conferma');
my $pw1M= $page->param('pw1M');
my $pw2M= $page->param('pw2M');
my $oldPw= $page->param('oldPw');

if($usrCurr && $tmpUserM1 eq $usrCurr || $tmpUserM2 eq $usrCurr){
    if($ok eq "Cambia"){
        my $fileXML="../data/user.xml";
        my $parser= XML::LibXML->new();
        my $doc= $parser->parse_file($fileXML) || die ("fail parser");
        my $root= $doc->getDocumentElement || die("fail radice");

        my $elemM= $doc->findnodes("//utente[email=\"$tmpUserM2\"]")->get_node(1);
        $nome= $elemM->findnodes("nome")->get_node(1)->textContent;
        $cogn= $elemM->findnodes("cognome")->get_node(1)->textContent;
        $pwd= $elemM->findnodes("pwd")->get_node(1)->textContent;
        $nick= $elemM->findnodes("nickname")->get_node(1)->textContent;
        #controllo password e cambiamento
        if($pw1M eq $pw2M && $oldPw eq $pwd){
            my $parent= $elemM->parentNode;
            $parent->removeChild($elemM);

            my $frammento= "
            <utente>
                <nome>".$nome."</nome>
                <cognome>".$cogn."</cognome>
                <nickname>".$nick."</nickname>
                <email>".$tmpUserM2."</email>
                <pwd>".$pw1M."</pwd>
            </utente>";

            my $nodo= $parser->parse_balanced_chunk($frammento) ||die("fail frammento");
            my $padre= $root;

            $padre->appendChild($nodo) || die("fail append");
            open(OUT, ">$fileXML");
            print OUT $doc->toString;
            close(OUT);

            $session->clear(["~logged-in", "tmpUserM"]);
            &printHeader("Cambio Password avvenuto");
            print'<h3>CAMBIO AVVENUTO CORRETTAMENTE</h3>';
            &printFooter;
        }
        else{
            #ERRORE DELLE PASSWORD
            &printHeader("ERRORE Cambio Password");
            print'<h3 class="errori">ERRORE</h3>';
            if($oldPw ne $pwd){
                print '<h3 class="errori">La vecchia <span xml:lang=\'en\'>password</span> non coincide!</h3>';
            }
            if($pw1M ne $pw2M){
                print'<h3 class="errori">Le nuove <span xml:lang=\'en\'>password</span> NON COINCIDONO!</h3>';
            }
            $session->clear(["~logged-in", "tmpUserM"]);
            print '<a href="cambioPwd.cgi?usr='.$tmpUserM2.'">Torna indietro</a>';
            &printFooter;
            exit;
        }
    }
    else{
        &printHeader("Dati Cambio Password");
        $session->param("tmpUserM", $tmpUserM1);
        print'<div> <form action="cambioPwd.cgi" method="post">
                    <fieldset>
                        <legend>Inserire la vecchia e la nuova <span xml:lang=\'en\'>Password</span></legend>
                        <label>Vecchia <span xml:lang=\'en\'>Password</span> <input tabindex="26" type="password" name="oldPw" /></label><br/>
                        <label>Nuova <span xml:lang=\'en\'>Password</span> <input tabindex="27" type="password" name="pw1M" /></label><br/>
                        <label>Ripetere <span xml:lang=\'en\'>Password</span> <input tabindex="28" type="password" name="pw2M" /></label><br/>
                        <input tabindex="29" type="submit" value="Cambia" name="conferma" />
                        <input tabindex="30" type="reset" value="Reset" />
                    </fieldset>
        </form></div>';
        &printFooter;
    }
}
else{
    &printHeader("ERRORE autenticazione");
    print' <div>
                <h3 class="errori">STAI TENTANDO DI CAMBIARE LA <span xml:lang=\'en\'>PASSWORD</span> DI UN ALTRO UTENTE!!</h3>
    </div>';
    $session->clear(["~logged-in", "tmpUserM"]);
    &printFooter;
    exit;
}
