  #!/usr/bin/env bash

## Read Configuration-File
. $PWD/lnd-invoicetoqr.config

## Start Logging
echo "####START CheckInvoice" >> $var_logPath

## Logging
echo "Variablen gesetzt" >> $var_logPath

## Logging
echo "Beginn Schleife" >> $var_logPath

## Declare variables with payment_request and r_hash
var_payReq=$(cat $var_tempPath/tempInvoice.txt | grep pay_req | cut -d '"' -f 4)
var_rHash=$(cat $var_tempPath/tempInvoice.txt | grep r_hash | cut -d '"' -f 4)

## Logging
echo "tempinvoice ausgelesen" >> $var_logPath

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
echo "####END CheckInvoice" >> $var_logPath
exit 0
