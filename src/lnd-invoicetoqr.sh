#!/bin/bash

## Grundlegende Variablen definieren, diese können/müssen systemspezifisch angepasst werden.
var_programDir=/home/<username>/lnd
var_macaroonPath=/home/<username>/lnd/invoice.macaroon
var_tlsCertPath=/home/<username>/lnd/tls.cert
var_rpcServer=<ipadress>:10009

## Folgende Variablen nicht aendern, ausser du weisst wirklich was du tust!
var_invoiceSat=$1
var_invoiceMemo=$2
var_paymentState=0
var_tempPath=$var_programDir/temp
var_lncliCommand="lncli --macaroonpath $var_macaroonPath --tlscertpath $var_tlsCertPath --rpcserver $var_rpcServer"

## Aktuell nicht in Benutzung befindliche Variablen
#var_lndLog=/home/bitcoin/.lnd/logs/bitcoin/mainnet/lnd.log

## Verzeichnis erstellen in dem später temporär Dateien abgelegt werden
mkdir -p $var_tempPath

## Prüfen ob der Invoice eine Memo mitgegeben wurde. Falls ja etwas umformatieren damit die Ausgabe
## bei erfolgter Zahlung etwas schöner aussieht
if [[ "$var_invoiceMemo" ]]; then
  var_invoiceMemo=", Memo: $var_invoiceMemo"
fi

## Prüfen ob ein Betrag an das Script übergeben werden, falls nicht abbrechen.
## In Bezug auf Hector hat dies nur Debugging Zwecke bzw. dient der Entwicklung/Tests
if [ $# -eq 0 ]
  then
	echo ""
	echo "Du musst mir schon sagen wie hoch die Rechnung sein soll. ;-)"
	echo ""
  exit 1
  else

  ## Invoice erstellen und die Infos payment_request und r_hash in die Datei schreiben
	$var_lncliCommand addinvoice $var_invoiceSat --memo "$2" > $var_tempPath/tempInvoice.txt

  ## Aus der soeben geschriebenen Datei werden nun payment_request und r_hash in Variablen geschrieben
	var_payReq=$(cat $var_tempPath/tempInvoice.txt | grep pay_req | cut -d '"' -f 4)
	var_rHash=$(cat $var_tempPath/tempInvoice.txt | grep r_hash | cut -d '"' -f 4)

  ## Für Debugging und Entwicklung den QR-Code auf der Konsole ausgeben
  qrencode -t ANSIUTF8 $var_payReq
  echo ""
  ## QR-code erstellen und als png ablegen, dieser muss dann 'irgendwie' auf das Display von Hector
  qrencode -o $var_tempPath/tempQRCode.png $var_payReq
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
COUNTER=0
while [  $COUNTER -lt 12 ]; do
  var_paymentState=$($var_lncliCommand lookupinvoice $var_rHash | grep state | cut -d '"' -f 4)
  if [[ $var_paymentState = "SETTLED" ]]
  then
                echo ""
                echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                echo ""
                echo "Invoice bezahlt, Betrag: $var_invoiceSat Satoshi$var_invoiceMemo"
                echo ""
                echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                exit 0
                break;
  else
                echo "Warte auf Zahlung... ($COUNTER)"
                sleep 5
  fi
let COUNTER=COUNTER+1
done

## Temp-Verzeichnisse löschen
rm -rf $var_tempPath
