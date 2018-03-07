#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&printHeader("Gioca da noi");
print'<div id="chiSiamo">
            <h1>QUATTRO POSTAZIONI DI GIOCO CON LE PRINCIPALI CONSOLE</h1>
            Gioca da noi da solo o in compangnia a tutti i giochi usati disponibili e ad alcuni gi&agrave; in prova al day one!
            Le console a cui &egrave; possibile giocare sono: Playstation 4, Xbox One, Playstation 3 ed Xbox 360<br/>
            <img src="../immagini/photo2.jpg" alt="postazioni di gioco"/>
            <p>Ecco il regolamento per utilizzare le postazioni:</p>
            <ul>
                <li>prezzo simbolico di 1&euro; all\'ora per le console, 2&euro; all\'ora per le console next generation</li>
                <li>se il gioco vi ha preso e volete continuare a giocare potete farlo a patto che non sia prenotata da qualcuno</li>
                <li>se deciderete di acquistare uno dei titoli provati avrete uno sconto pari a ci&ograve; che avete speso provandolo!</li>
            </ul>
            <h2>Inoltre se siete nostalgici abbiamo a disposizione un\'intera collezione di retro-games disponibili all\'utenza</h2>
      </div><!-- chi siamo chiusura-->';
&printFooter;
exit;
