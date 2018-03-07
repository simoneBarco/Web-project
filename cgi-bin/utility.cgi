#!/usr/bin/perl
use CGI; # importa la libreria CGI
use CGI::Session();
use HTML::Entities;
use CGI::Carp qw(fatalsToBrowser);
#use utf8;
#no utf8;
use Switch;

sub createSession(){
    $session=new CGI::Session() or die "errore sessione";
    $session->param('utente', @_[0]);
    print $session->header(-location=>@_[1]);
}

sub getSession(){
    my $session=CGI::Session->load() or die "sessione non trovata";
    if($session->is_expired || $session->is_empty){
        return "";
    }
    else{
        my $utente=$session->param("utente");
        return $utente;
    }
}

sub destroySession(){
    $session=CGI::Session->load() or die $!;
    $SID=$session->id();
    $session->close();
    $session->delete();
    $session->flush();
}

sub printHeader{
    $session=CGI::Session->load() or die "sessione non trovata";
    my $page=new CGI;
    print $page->header(-charset=>'utf-8');
    #print '
    print <<EOF;
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="it" lang="it">
    <head>
        <meta http-equiv="Content-Type" content="text/html charset=utf-8" />
        <title>
EOF
    if($_[0] eq "Home"){
        print "GameSide";
    }
    else{
        print @_[0]."-GameSide";
    }
    print '</title>
    <meta name="author" content="HardPerlTeam" />
    <meta name="description" content="GameSIDE è insieme un negozio di videogiochi ed un centro del divertimento per tutti gli appassionati di questo settore" />
    <meta name="keywords" content="gameside, giochi, padova, eventi, torneo, postazioni, console, pc, xbox, playstation, nintentdo"/>
    <meta name="language" content="italian it" />';
    #STAMPARE META AUTHOR, DESCRIPTION, KEYWORD
    if(index(@_[0],"Aggiunta commento") != -1){
        $session= CGI::Session->load() or die "sessione non trovata";
        my $idComm= $session->param('idComm');
        print '<meta http-equiv="refresh" content="0; URL=eventi.cgi?id='.$idComm.'"></meta>';
    }
    if(@_[0] eq "Bentornato" || @_[0] eq "Logout"){
        print '<meta http-equiv="refresh" content="0; URL=index.cgi"></meta>';
    }
    if(@_[0] eq "Cancellazione commento"){
        $session= CGI::Session->load() or die "sessione non trovata";
        my $idE= $session->param('idEelim');
        print '<meta http-equiv="refresh" content="1; URL=eventi.cgi?id='.$idE.'"></meta>';
    }
    print"
    <link href=\"../css/main.css\" rel=\"stylesheet\" type=\"text/css\" />";
    if(@_[0] eq "Registrazione"){
        print'<meta http-equiv="Content-Script-Type" content="text/javascript"/>
            <script type="text/javascript" src="../js/script.js"></script>';
    }
    if(@_[0] eq "Nuovo/Modifica gioco" || @_[0] eq "Nuovo/Modifica evento" || @_[0] eq "ERRORE Evento" || @_[0] eq "ERRORE Gioco/Console"){
        print'<meta http-equiv="Content-Script-Type" content="text/javascript"/>
        <script type="text/javascript" src="../js/script2.js"></script>';
    }

    print'</head>

    <body>
    <div id="main_container">
        <div id="top" class="shadows">
            <div id="top_section" class="panels, shadows">';
                if(@_[0] ne "Home"){
                    print'<div id="logoBox">
                        <h1 id="logo"><a tabindex="1" href="/tecweb/~sbarco/cgi-bin/index.cgi">
                        <span id="p1">Game</span><span id="p2">Side</span></a> </h1>
                        <h2>vivi il lato migliore del gioco</h2>
                    </div><!--chiusura logoBox-->';
                }
                else{
                    print'<div id="logoBox">
                        <h1>
                        <span id="p1">Game</span><span id="p2">Side</span></h1>
                        <h2>vivi il lato migliore del gioco</h2>
                    </div><!--chiusura logoBox-->';
                }
                print'<div id="loginBox">';
                    &printForm;
                    print'
                </div><!--chiusura loginBox-->
                <br class="clearFloat" />
            </div><!-- end top_section -->

            <div id="bottom_section">
                <div id="map" class="panels, shadows">';
                    &printPath;
                    print'<form action="ricerca.cgi" method="get">
                            <div>
                                <input title="searchbar" tabindex="8" id="searchbar" type="text" name="search"/>
                                <input title="searchbutton" tabindex="9" id="searchbutton" type="submit" value="Cerca" />
                            </div>
                    </form>';
                print'</div><!--chiusura map-->
            </div><!-- end bottom_section -->
        </div> <!--end top -->
        <div id="content_container">
            <div id="center" class="panels, shadows">
                <a class="nascosto" href="#content">Salta il men&ugrave;</a>
                <div id="menuButton"><input title="mcb" type="checkbox" id="mcb" checked="checked" />
                    <div id="left" class="panels, shadows">
                        <ul>';
                        if(@_[0] eq "Home"){
                            print '<li><h1 id="pageCurr"><span xml:lang=\'en\'>Home</span></h1></li>';
                        }
                        else{
                            print '<li><h1><a tabindex="9" href="index.cgi"><span xml:lang=\'en\'>Home</span></a></h1></li>';
                        }
                        if(@_[0] eq "Chi siamo"){
                            print'<li><h1 id="pageCurr">Chi siamo</h1></li>';
                        }
                        else{
                            print'<li><h1><a tabindex="10" href="chisiamo.cgi">Chi siamo</a></h1></li>';
                        }
                        if(@_[0] eq "Giochi"){
                            print'<li><h1 id="pageCurr">Giochi</h1></li>';
                        }
                        else{
                            print'<li><h1><a tabindex="11" href="menu.cgi?cg=1">Giochi</a></h1></li>';
                        }
                        if(@_[0] eq "Lista giochi PC"){
                            print'<li><h2 id="pageCurr">PC</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="12" title="PC" href="giochi.cgi?ty=gpc">PC</a></h2></li>';
                        }
                        if(@_[0] eq "Lista giochi XBox"){
                            print'<li><h2 id="pageCurr">XBox</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="13" title="XBox" href="giochi.cgi?ty=gxbox">XBox</a></h2></li>';
                        }
                        if(@_[0] eq "Lista giochi PS4"){
                            print'<li><h2 id="pageCurr">PS4</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="14" title="PS4" href="giochi.cgi?ty=gps4">PS4</a></h2></li>';
                        }
                        if(@_[0] eq "Lista giochi Nintendo"){
                            print'<li><h2 id="pageCurr"><span id="pageCurr">Nintendo</span></h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="15" title="Nintendo" href="giochi.cgi?ty=gnin">Nintendo</a></h2></li>';
                        }
                        if(@_[0] eq "Console"){
                            print'<li><h1 id="pageCurr"><span xml:lang=\'en\'>Console</span></h1></li>';
                        }
                        else{
                            print'<li><h1><a tabindex="16" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span></a></h1></li>';
                        }
                        if(@_[0] eq "Lista Accessori PC"){
                            print'<li><h2 id="pageCurr">Accessori PC</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="17" title="AccessoriPC" href="giochi.cgi?ty=cpc">Accessori PC</a></h2></li>';
                        }
                        if(@_[0] eq "Lista console XBox"){
                            print'<li><h2 id="pageCurr">XBox</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="18" title="ConsoleXBox" href="giochi.cgi?ty=cxbox">XBox</a></h2></li>';
                        }
                        if(@_[0] eq "Lista console PS4"){
                            print'<li><h2 id="pageCurr">PS4</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="19" title="ConsolePS4" href="giochi.cgi?ty=cps4">PS4</a></h2></li>';
                        }
                        if(@_[0] eq "Lista console Nintendo"){
                            print'<li><h2 id="pageCurr">Nintendo</h2></li>';
                        }
                        else{
                            print'<li><h2><a tabindex="20" title="ConsoleNintendo" href="giochi.cgi?ty=cnin">Nintendo</a></h2></li>';
                        }
                        if(@_[0] eq "Gioca da noi"){
                            print'<li><h1 id="pageCurr">Gioca da noi</h1></li>';
                        }
                        else{
                            print'<li><h1><a tabindex="21" href="giocadanoi.cgi">Gioca da noi</a></h1></li>';
                        }
                        if(@_[0] eq "Lista eventi"){
                            print'<li><h1 id="pageCurr">Eventi</h1></li>';
                        }
                        else{
                            print'<li><h1><a tabindex="22" href="eventi.cgi">Eventi</a></h1></li>';
                        }
                        if(&getSession()){
                            if(@_[0] eq "Utente"){
                                print'<li id="loginLink"><h1 id="pageCurr"><span xml:lang=\'en\'>Utente</span></h1></li>';
                            }
                            else{
                                print'<li id="loginLink"><h1><a tabindex="22" href="loginMob.cgi"><span xml:lang=\'en\'>Utente</span></a></h1></li>';
                            }
                        }
                        else{
                            if(@_[0] eq "Login"){
                                print'<li id="loginLink"><h1 id="pageCurr"><span xml:lang=\'en\'>Login</span></h1></li>';
                            }
                            else{
                                print'<li id="loginLink"><h1><a tabindex="22" href="loginMob.cgi"><span xml:lang=\'en\'>Login</span></a></h1></li>';
                            }
                        }
                        print'
                        </ul>

                    </div><!--chiusura left-->
                </div><!--chiusura menuButton-->
            <div id="content">
            ';
  }


sub printPath{
    print '<p>Ti trovi in ';
    if(@_[0] eq "Home"){
        print '<span xml:lang=\'en\'>Home</span></p>';
    }
    elsif(@_[0] eq "Registrazione"){
        print 'Registrazione</p>';
    }
    elsif(@_[0] eq "Login"){
        print' Login</p>';
    }
    elsif(@_[0] eq "Utente"){
        print'Utente</p>';
    }

    elsif(@_[0] eq "Giochi"){
        print 'Giochi</p>';
    }
    elsif(@_[0] eq "Console"){
        print '<span xml:lang=\'en\'>Console</span></p>';
    }
    elsif(@_[0] eq "Amministrazione"){
        print 'Amministrazione</p>';
    }
    elsif(@_[0] eq "Nuovo/Modifica gioco"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica gioco</p>';
    }
    elsif(@_[0] eq "Nuovo/Modifica evento"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica evento</p>';
    }
    elsif(@_[0] eq "Lista eventi"){
        print 'Eventi</p>';
    }
    elsif(@_[0] eq "Lista giochi PC"){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; PC</p>';
    }
    elsif(@_[0] eq "Lista giochi XBox"){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; XBox</p>';
    }
    elsif(@_[0] eq "Lista giochi PS4"){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; PS4</p>';
    }
    elsif(@_[0] eq "Lista giochi Nintendo"){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; Nintendo</p>';
    }
    elsif(@_[0] eq "Lista Accessori PC"){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; Accessori PC</p>';
    }
    elsif(@_[0] eq "Lista console XBox"){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; XBox</p>';
    }
    elsif(@_[0] eq "Lista console PS4"){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; PS4</p>';
    }
    elsif(@_[0] eq "Lista console Nintendo"){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; Nintendo</p>';
    }
    elsif(@_[0] eq "Chi siamo"){
        print 'Chi siamo</p>';
    }
    elsif(@_[0] eq "Dati Cambio Password"){
        print 'Cambio <span xml:lang=\'en\'>Password</span></p>';
    }
    elsif(@_[0] eq "ERRORE Cambio Password"){
        my $usr= &getSession();
        print '<a href="cambioPwd.cgi?usr='.$usr.'">Cambio <span xml:lang=\'en\'>Password</span></a> -&gt; Errore Cambio Password</p>';
    }
    elsif(@_[0] eq "Cambio Password avvenuto"){
        my $usr= &getSession();
        print '<a href="cambioPwd.cgi?usr='.$usr.'">Cambio <span xml:lang=\'en\'>Password</span></a> -&gt; Cambio Password avvenuto</p>';
    }

    elsif((rindex @_[0], "Accessori PC") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; <a tabindex="7" title="Accessori PC" href="giochi.cgi?ty=cpc">Accessori PC </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "Console XBox") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; <a tabindex="7" title="Console XBox" href="giochi.cgi?ty=cxbox">XBox </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "Console PS4") != -1){
        print '<a href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; <a tabindex="7" title="Console PS4" href="giochi.cgi?ty=cps4">PS4 </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "Console Nintendo") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=2"><span xml:lang=\'en\'>Console</span> </a> -&gt; <a tabindex="7" title="Console Nintendo" href="giochi.cgi?ty=cnin">Nintendo </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "PC") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; <a tabindex="7" title="PC" href="giochi.cgi?ty=gpc">PC </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "XBox") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; <a tabindex="7" title="XBox" href="giochi.cgi?ty=gxbox">XBox </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "PS4") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; <a tabindex="7" title="PS4" href="giochi.cgi?ty=gps4">PS4 </a> -&gt; '.@_[0].'</p>';
    }
    elsif((rindex @_[0], "Nintendo") != -1){
        print '<a tabindex="6" href="menu.cgi?cg=1">Giochi </a> -&gt; <a tabindex="7" title="Nintendo" href="giochi.cgi?ty=gnin">Nintendo </a> -&gt; '.@_[0].'</p>';
    }
    elsif (@_[0] eq "ERRORE Evento"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica evento -&gt; Errore Evento</p>';
    }
    elsif(@_[0] eq "Caricamento Evento"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica evento -&gt; Caricamento Evento</p>';
    }
    elsif((rindex @_[0], "Evento") != -1){
        print '<a tabindex="6" href="eventi.cgi">Eventi </a> -&gt; '.@_[0].'</p>';
    }
    elsif(@_[0] eq "Gioca da noi"){
        print 'Gioca da noi</p>';
    }
    elsif (@_[0] eq "ERRORE Gioco/Console"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica gioco -&gt; Errore Gioco/Console</p>';
    }
    elsif(@_[0] eq "Caricamento Gioco/Console"){
        print '<a tabindex="6" href="gestioneAd.cgi">Amministrazione </a> -&gt; Nuovo/Modifica gioco -&gt; Caricamento Gioco/Console</p>';
    }

    elsif(@_[0] eq "Conferma eliminazione Evento" || @_[0] eq "Cancellazione Evento"){
        print '<a tabindex="6" href="eventi.cgi">Eventi </a> -&gt; Cancellazione '.@_[0].'</p>';
    }
    elsif(@_[0] eq "Conferma eliminazione Gioco/Console" || @_[0] eq "Cancellazione Gioco/Console"){
        print 'Cancellazione Gioco/Console</p>';
    }
    elsif(index(@_[0], "Aggiunta commento") != -1){
        print '<a tabindex="6" href="eventi.cgi">Eventi </a> -&gt; Aggiunta Commento</p>';
    }
    elsif(@_[0] eq "ERRORE autenticazione"){
        print 'Errore di autenticazione</p>';
    }
    elsif(@_[0] eq "Cancellazione commento" || @_[0] eq "Conferma eliminazione commento"){
        print'Cancellazione commento</p>';
    }
    elsif(index(@_[0], "Risultati per") != -1){
        print'Risultati ricerca</p>';
    }
    elsif(@_[0] eq "ERRORE Registrazione"){
        print '<a tabindex="6" href="registrazione.cgi">Registrazione</a> -&gt; Errore Registrazione</p>';
    }
    elsif(@_[0] eq "Registrazione effettuata"){
        print '<a tabindex="6" href="registrazione.cgi">Registrazione</a> -&gt; Registrazione effettuata</p>';
    }
    elsif(@_[0] eq "ERRORE Login"){
        print'Errore login</p>';
    }
    elsif(@_[0] eq "Logout"){
        print'Logout</p>';
    }
    elsif(@_[0] eq "Bentornato"){
        print'Bentornato</p>';
    }

}

sub printFooter{
    my $page=new CGI;
    print '
    </div><!--chiusura content-->
    <br class="clearFloat"/>
    </div><!--chiusura center-->
    <a href="#" id="goTop">Go to top</a>
    <div id="footer" class="panels, shadows">
        <div>
            <h1>GameSide</h1>
            <ul>
                <li><h2>Via degli Zabarella, 22 Padova</h2></li>
                <li><h2>Tel: 049 2612306</h2></li>
                <li><h2>Cell: 377 5069819</h2></li>
            </ul>
        </div>
        <div>
            <h1>Orario</h1>
            <ul>
                <li><h2>luned&igrave;-venerd&igrave; : 9:30-19:30</h2></li>
                <li><h2>sabato: 10:00-19:30</h2></li>
                <li><h2>domenica: 15:00-19:30</h2></li>
            </ul>
        </div>
        <div>
            <a href="http://validator.w3.org/check?uri=referer">
                <img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" />
            </a>
            <a href="http://jigsaw.w3.org/css-validator/check/referer">
                <img style="border:0;width:88px;height:31px" src="http://jigsaw.w3.org/css-validator/images/vcss" alt="CSS Valido!" />
            </a>
            <img src="../immagini/valid_xhtml_10.gif" alt="Valid XHTML 1.0 Strict by Total Validator" height="31" width="88" />
        </div>
        <br class="clearFloat"/>
    </div><!--chiusura footer-->
    </div><!--chiusura content_container-->
</div><!--chiusura main_container-->';

print $page->end_html;
}

sub printForm(){
    my $tmpUser=getSession();
    if($tmpUser eq ""){
        print '<form action="login.cgi" method="post">
                    <fieldset>
                        <legend> Accedi compilando il form</legend>
                        <label>Utente <input tabindex="2" type="text" name="email" /></label><br/>
                        <label><span xml:lang=\'en\'>Password</span> <input tabindex="3" type="password" name="pwd" /></label><br/>
                        <input tabindex="4" type="submit" value="Login" />
                        <a tabindex="5" href="registrazione.cgi">Registrazione</a>
                    </fieldset>
        </form>'
    }
    else{
        if($tmpUser eq 'admin@mail.com'){
                print 'Bentornato Admin<br/>';
                if(@_[0] eq "Amministrazione"){
                    print 'Amministrazione<br />';
                }
                else{
                    print '<a tabindex="2" href="gestioneAd.cgi">Amministrazione</a><br/>';
                }
        }
        else{
            print 'Bentornato '.$tmpUser.'<br/>';
        }
        if(@_[0] eq "Dati Cambio Password"){
            print'Cambio Password';
        }
        else{
            print'<a tabindex="3" href="cambioPwd.cgi?usr='.$tmpUser.'">Cambio <span xml:lang=\'en\'>Password</span> </a>';
        }
        print '<br /><a tabindex="4" href="logout.cgi">Logout</a>';

    }
}
1;
