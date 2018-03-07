#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&printHeader("Registrazione");
my $page= new CGI;
if(&getSession()){
    print'<h3 class="errori">Sei gi&agrave; autenticato!</h3>';
}
else{
    print '<h2>Iscrizione a GameSide</h2>
            <form id="reg" action="join.cgi" method="post">
                <fieldset><legend>Compilare i seguenti campi in modo opportuno</legend>
                    <label>Nome:
                        <input type="text" name="nome" tabindex="26" id="in"  /><span id="nome"></span><br />
                    </label>
                    <label>Cognome:
                        <input type="text" name="cognome" tabindex="27" id="ic"  /><span id="cognome"></span><br />
                    </label>
                    <label>Nickname:
                        <input type="text" name="nickname" tabindex="28" id="ni"  /><br />
                    </label>
                    <label>E-mail:
                        <input type="text" name="email" tabindex="29" id="ie"  /><span id="email"></span><br />
                    </label>
                    <label>Password:
                        <input type="password" name="pw1" tabindex="30" id="ip1"  /><span id="pwd1"></span><br />
                    </label>
                    <label>Ripetere la password:
                        <input type="password" name="pw2" tabindex="31" id="ip2"  /><span id="pwd2"></span><br />
                    </label>
                    <input type="submit" name="Registrati" tabindex="32" />
                </fieldset>
            </form>';

}
&printFooter;
exit;
