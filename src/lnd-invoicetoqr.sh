#!/bin/bash

## Konfiguration einlesen
. /home/pi/Hector9000/src/lnd-invoicetoqr.config

## Logging beginnen
echo "####START" >> $var_logPath

## Logging
echo "Variablen gesetzt" >> $var_logPath

## Aktuell nicht in Benutzung befindliche Variablen
#var_lndLog=/home/bitcoin/.lnd/logs/bitcoin/mainnet/lnd.log

## Verzeichnis erstellen in dem später temporär Dateien abgelegt werden
mkdir -p $var_tempPath

## Logging
echo "temppath gelöscht" >> $var_logPath

## Relevante Dateien löschen
rm -f $var_tempPath/ok.txt >> $var_logPath
rm -f $var_tempPath/tempQRCode.png >> $var_logPath
rm -f $var_tempPath/tempInvoice.txt >> $var_logPath

## Prüfen ob der Invoice eine Memo mitgegeben wurde. Falls ja etwas umformatieren damit die Ausgabe
## bei erfolgter Zahlung etwas schöner aussieht
if [[ "$var_invoiceMemo" ]]; then
  var_invoiceMemo=", Memo: $var_invoiceMemo"
fi

## Prüfen ob ein Betrag an das Script übergeben werden, falls nicht abbrechen.
## In Bezug auf Hector hat dies nur Debugging Zwecke bzw. dient der Entwicklung/Tests
if [ $var_invoiceSat -eq 0 ]
  then
	echo ""
	echo "Du musst mir schon sagen wie hoch die Rechnung sein soll. ;-)"
	echo ""
  exit 1
  else

## Logging
echo "invoicesat prüfung abgeschlossen" >> $var_logPath

  ## Invoice erstellen und die Infos payment_request und r_hash in die Datei schreiben
	$var_lncliCommand addinvoice $var_invoiceSat --memo "$2" > $var_tempPath/tempInvoice.txt

## Logging
echo "lnclicommand" >> $var_logPath

  ## Aus der soeben geschriebenen Datei werden nun payment_request und r_hash in Variablen geschrieben
	var_payReq=$(cat $var_tempPath/tempInvoice.txt | grep pay_req | cut -d '"' -f 4)
	var_rHash=$(cat $var_tempPath/tempInvoice.txt | grep r_hash | cut -d '"' -f 4)

## Logging
echo "tempinvoice ausgelesen" >> $var_logPath

  ## Für Debugging und Entwicklung den QR-Code auf der Konsole ausgeben
  qrencode -t ANSIUTF8 $var_payReq
  echo ""

## Logging
echo "QRCode ausgabe auf cli" >> $var_logPath

  ## QR-code erstellen und als png ablegen, dieser muss dann 'irgendwie' auf das Display von Hector
  qrencode -o $var_tempPath/tempQRCode.png $var_payReq

## Logging
echo "tempQRCode abgelegt" >> $var_logPath

fi

## Alte Tests zu Bildschirmausgaben, einfach ignorieren
#fim $var_tempPath/tempQRCode.png
#fim -a -T 1 -d /dev/fb0 $var_tempPath/tempQRCode.png
#fbi -a --noverbose -T 1 $var_tempPath/tempQRCode.png

## Eine Minute lang darauf warten ob die Invoice bezahlt wurde
## dazu alle 10 Sekunden mittels lookupinvoice schauen ob der STATE der Zahlung SETTLED ist
## die Wartezeit zwischen zwei lookupinvoice sollte gemäß der Internetverbindung getestet und angepasst werden.
## Das könnte man auch vorab im Script testen und die Geschwindigkeit dann variabel anpassen, falls nötig.
## Die echo's dienen nur dem Debugging/Testing auf der Konsole

## Logging
echo "Beginn Schleife" >> $var_logPath

COUNTER=0
while [  $COUNTER -lt 2 ]; do
  var_paymentState=$($var_lncliCommand lookupinvoice $var_rHash | grep state | cut -d '"' -f 4)
## Logging
echo "lookupinvoice" >> $var_logPath

  if [[ $var_paymentState = "SETTLED" ]]
  then
                echo ""
                echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                echo ""
                echo "Invoice bezahlt, Betrag: $var_invoiceSat Satoshi$var_invoiceMemo"
                echo ""
                echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                touch $var_tempPath/ok.txt
## Logging
echo "payment settled" >> $var_logPath


                exit 0
  else
                echo "Warte auf Zahlung... ($COUNTER)"
## Logging
echo "warte auf zahlung $COUNTER" >> $var_logPath

                sleep 5
  fi
let COUNTER=COUNTER+1
done

## Logging
echo "ENDE Schleife" >> $var_logPath

## Temp-Verzeichnisse löschen
#rm -rf $var_tempPath

## Logging
echo "ENDE SCRIPT" >> $var_logPath
exit 0
