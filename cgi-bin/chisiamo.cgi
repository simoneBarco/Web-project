#!/usr/bin/perl
use CGI;
use XML::LibXML;
use HTML::Entities;
require "utility.cgi";
&printHeader("Chi siamo");
my $page= new CGI;
print'<div id="chiSiamo">
            <h1>GameSIDE &egrave; insieme un negozio di videogiochi ed un centro del divertimento per tutti gli appassionati di questo settore.</h1>
            <h2>Siamo aperti dal 2011 e siamo l\'unico negozio di videogiochi presente nel centro storico di Padova.</h2>

            <img src="../immagini/photo1.jpg" alt="entrata negozio"/>
            Da noi &egrave; possibile trovare videogiochi nuovi ed usati ed ordinare qualsiasi titolo non disponibile in negozio destinato
            al mercato europeo. Si possono inoltre permutare i propri videogiochi/le proprie console per l\'acquisto di altri videogiochi nuovi/usati,
            console, accessori o qualsiasi prodotto disponibile in negozio. <br/>
            Il nostro impegno &egrave; quello di offrire la migliore valutazione possibile per i videogiochi rientrati ed il prezzo pi&ugrave; basso per i
            prodotti che vendiamo. <br/>
            Il risparmio &egrave; ancora maggiore con la nostra Premium Card che, per un anno,
            al costo di soli 5 euro, permette di risparmiare su qualsiasi acquisto/preordine
            e avere molti vantaggi.<br/>
            <div id="panelRegolamento">Regolamento:
                        <h1> SCONTI SU TUTTI I TUOI ACQUISTI DI VIDEOGIOCHI</h1>
                        Grazie alla tua Premium Card puoi risparmiare ulteriormente ottenendo sconti su tutti i videogiochi (nuovi ed usati) ogni volta
                        che la utilizzi:
                        <ul>
                            <li>1 euro di sconto ogni volta che acquisti un gioco;</li>
                            <li>9 euro di sconto totali (cio&egrave; 3 euro per gioco) con l\'acquisto di tre giochi nello stesso momento;</li>
                            <li>4 euro di sconto totali (cio&egrave; 2 euro per gioco) con l\'acquisto di due giochi nello stesso momento;</li>
                            <li>12 o pi&ugrave; euro di sconto totali (3 euro per gioco) con l\'acquisto di quattro o pi&ugrave; giochi nello stesso momento.</li>
                        </ul>
                        Lo sconto &egrave; applicabile a tutti i giochi presenti in negozio. Non &egrave; applicabile ai giochi con un prezzo inferiore a 4,50 &euro;,
                        ai retrogames ed ai giochi in preordine (questi ultimi, per i possessori di Premium Card, hanno uno sconto addirittura maggiore).

                        Acquista pi&ugrave; giochi con i tuoi amici. Con una sola card (ne basta una per un gruppo) potete avere fino a 3 euro di sconto per ogni gioco.

                        <h1>PREORDINI</h1>
                        Con la Premium Card puoi preordinare i tuoi videogiochi preferiti assicurandoti uno sconto di almeno 5 euro su tutti i giochi in
                        uscita (con prezzo maggiore di 30 &euro;). Per farlo ti baster&agrave; inviarci una mail, un sms o telefonarci indicando il tuo numero di Premium Card
                        (hai sempre a disposizione i nostri recapiti sul retro della tua card) ed indicando i giochi che vuoi ricevere (fino a 3 giorni precedenti
                        l\'uscita del gioco).

                        <h1>RICARICATI DI 50 CENTESIMI OGNI 10 EURO SPESI</h1>
                        Ogni 10 euro di spesa in videogiochi (nuovi o usati) ricevi 50 centesimi di credito da spendere per qualsiasi acquisto successivo
                        (ad eccezione dei preordini per cui c\'&egrave; uno sconto immediato di almeno 5 euro).

                        <h1>IN UNA CARTA IL TUO CREDITO CHE NON SCADE MAI</h1>
                        Tutto il credito maturato rientrando da noi il tuo usato, oppure accumulato grazie alle &quot;ricariche&quot; per ogni 10 euro di spesa,
                        viene conservato nella tua Premium Card.
                        Non devi utilizzarlo in un\'unica volta e non hai una scadenza per utilizzarlo.
                        Puoi utilizzare il tuo credito anche per giocare da noi o iscriverti ai nostri tornei!

                        <h1>OFFERTE RISERVATE - PREZZO SCONTATO PER I POSSESSORI DELLA PREMIUM CARD</h1>
                        I prezzi di alcuni videogiochi, durante l\'anno, hanno un ulteriore sconto esclusivamente per i possessori della Premium Card.
                        In negozio vengono evidenziati i giochi che hanno uno sconto esclusivo, riservato ai possessori della Card.

                        <h1>LINEA DIRETTA GAMESIDE</h1>
                        Con la Premium Card hai il tuo negozio di videogame sempre a portata di mano.
                        Sulla Card trovi tutti i nostri recapiti che potrai utilizzare per:
                        <ul>
                            <li> richiederci informazioni;</li>
                            <li> avere una valutazione immediata dei tuoi videogiochi usati (anche telefonicamente, per e-mail o sms).</li>
                        </ul>
                        In questo modo potrai ordinare e preordinare i tuoi giochi preferiti telefonicamente, via sms, e-mail oppure tramite
                        la nostra pagina Facebook e Skype.
                        <br/>
            </div>
            Ma per noi non &egrave; importante solo il risparmio. E\' fondamentale la soddisfazione del cliente ed il rapporto che abbiamo con tutta la gente GameSIDE.
            Per questo motivo non vendiamo mai, per esempio, un gioco nuovo gi&agrave; aperto come capita spesso purtroppo in altre realt&agrave; del settore.
            Per lo stesso motivo diamo la possibilit&agrave; di provare i giochi prima di acquistarli o semplicemente per divertirsi con gli amici. <br/>

            Il &quot;centro del divertimento&quot; ha, infatti, il suo fulcro nelle nostre &quot;Demo stations&quot;, postazioni TV con le principali console (PS4, Xbox One, PS3 ed
            Xbox 360) con cui &egrave; possibile: <br/>
            <ul>
                <li> provare i migliori videogiochi anche prima della loro uscita;</li>
                <li> giocare con gli amici a tutti i giochi disponibili in negozio;</li>
                <li> partecipare ai tornei dei giochi pi&ugrave; divertenti o agli eventi a tema.</li>
            </ul><br/>
            Siamo in centro a Padova in via degli Zabarella, 22 <br/>
            Come raggiungerci?<br/>
            <ul>
                <li>TRAM<br/>
                Se raggiungi il centro in tram la fermata pi&ugrave; vicina &egrave; &quot;Ponti Romani&quot;.
                Parallela a Riviera dei Ponti Romani, quindi vicinissima alla fermata, c\'&egrave; via degli Zabarella.
                Noi siamo quasi all\'incrocio con via Cesare Battisti.
                </li>

                <li>AUTO<br/>
                Arrivando in centro in auto il parcheggio pi&ugrave; vicino &egrave; quello di via San Biagio che si trova a 300 metri dal negozio.
                E\' aperto tutti i giorni dalle 7 alle 22.
                </li>

                <li>AUTOBUS<br/>
                Tutti gli autobus che passano per Riviera dei Ponti Romani hanno una fermata molto vicina al negozio.
                In ogni caso siamo facilmente raggiungibili dalla gan parte delle fermate del centro storico.
                </li>
            </ul>
            <div id="panelMappa">Mappa:
                    <!-- target="_blank" --><a href="https://www.google.it/maps/place/GameSIDE+Padova/@45.4064971,11.878765,18.75z/data=!4m5!3m4!1s0x477eda50bfff4821:0x5327691a7a52b3f9!8m2!3d45.4065407!4d11.8792819"><img src="../immagini/mappa.png" alt="mappa GameSide"/></a>
            </div>
            Teniamo molto anche agli eventi come, ad esempio, gli &quot;Streetpass Meeting&quot; Nintendo, i tornei dei giochi pi&ugrave; attesi ed altre occasioni di ritrovo
            per tutti gli appassionati. <br/>

            <p>
                Insomma ci sono tanti motivi per passare a trovarci e per &quot;vivere il lato migliore del gioco&quot;! 
            </p>
</div>';
&printFooter;
exit;
