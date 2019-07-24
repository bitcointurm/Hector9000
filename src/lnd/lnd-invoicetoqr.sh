#!/#!/usr/bin/env bash

## Read Configuration-File
. $PWD/lnd-invoicetoqr.config

## Start Logging
echo "####START" >> $var_logPath

## Logging
echo "Variablen gesetzt" >> $var_logPath

## Create temporary directory
mkdir -p $var_tempPath

## Logging
echo "temppath gelöscht" >> $var_logPath

## Delete unwanted/old files (should be changed to be done at the end of the script)
rm -f $var_tempPath/ok.txt >> $var_logPath
rm -f $var_tempPath/tempQRCode.png >> $var_logPath
rm -f $var_tempPath/tempInvoice.txt >> $var_logPath

## Check if amount is set. If not, exit.
if [ $var_invoiceSat -eq 0 ]
  then
	echo ""
	echo "Du musst mir schon sagen wie hoch die Rechnung sein soll. ;-)"
	echo ""
  exit 1
  else

## Logging
echo "invoicesat prüfung abgeschlossen" >> $var_logPath

  ## Create Invoice and print all iformation (mainly payment_request and r_hash) to file
	$var_lncliCommand addinvoice --amt $var_invoiceSat --memo "$var_invoiceMemo" > $var_tempPath/tempInvoice.txt

## Logging
echo "lnclicommand" >> $var_logPath

  ## Declare variables with payment_request and r_hash
	var_payReq=$(cat $var_tempPath/tempInvoice.txt | grep pay_req | cut -d '"' -f 4)
	var_rHash=$(cat $var_tempPath/tempInvoice.txt | grep r_hash | cut -d '"' -f 4)

## Logging
echo "tempinvoice ausgelesen" >> $var_logPath

  ## For Debugging and Development, print QR-Code to cli (STDOUT)
  qrencode -t ANSIUTF8 $var_payReq
  echo ""

## Logging
echo "QRCode ausgabe auf cli" >> $var_logPath

  ## Save QR-Code to file, this one is going to be visible to the customer
  qrencode -o $var_tempPath/tempQRCode.png $var_payReq

## Logging
echo "tempQRCode abgelegt" >> $var_logPath

fi

## Ignore, had been used at LightningHackdays MUC
#fim $var_tempPath/tempQRCode.png
#fim -a -T 1 -d /dev/fb0 $var_tempPath/tempQRCode.png
#fbi -a --noverbose -T 1 $var_tempPath/tempQRCode.png

## Wait a minute and check if invoice has been paid
## therefore use lookupinvoice every x seconds to see if STATE is SETTLED
## sleep between two lookupinvoice should be changed to meet internet-connectivity/speed of command
## This Speedtest could be checked by the script if needed in a future release

## Logging
echo "Beginn Schleife" >> $var_logPath

## Check if there is an Invoice Memo available, if so
## reformat for styling reasons (only to be used for cli output)
if [[ "$var_invoiceMemo" ]]; then
  var_invoiceMemo=", Memo: $var_invoiceMemo"
fi

COUNTER=0
while [  $COUNTER -lt 12 ]; do
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

## Remove Temporary-Directory
#rm -rf $var_tempPath

## Logging
echo "ENDE SCRIPT" >> $var_logPath
exit 0
