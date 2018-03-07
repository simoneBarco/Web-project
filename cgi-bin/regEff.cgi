#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";

&printHeader("Registrazione effettuata");
print '
            <h3>Registrazione effettuata!</h3>
            <h3>Grazie per esserti registrato! Ora potrai accedere a molte altre funzionalit&agrave;</h3>';
&printFooter;

exit;
