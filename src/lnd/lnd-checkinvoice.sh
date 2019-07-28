#!/usr/bin/env bash

## Read Configuration-File
. lnd/lnd-invoicetoqr.config

## Start Logging
echo "####START CheckInvoice" >> $var_logPath

## Logging
echo "Variablen gesetzt" >> $var_logPath

## Declare variables with payment_request and r_hash
var_rHash=$(cat $var_tempPath/tempInvoice.txt | grep r_hash | cut -d '"' -f 4)

## Logging
echo "tempinvoice ausgelesen" >> $var_logPath

## Check if there is an Invoice Memo available, if so
## reformat for styling reasons (only to be used for cli output)
if [[ "$var_invoiceMemo" ]]; then
  var_invoiceMemo=", Memo: $var_invoiceMemo"
fi

## Logging
echo "lookupinvoice" >> $var_logPath

## check invoice and write only SETTLED or OPEN to variable
var_paymentState=$($var_lncliCommand lookupinvoice $var_rHash | grep state | cut -d '"' -f 4)

## important part, as MainPanel.py is waiting to see 'SETTLED' on the command line
case $var_paymentState in
  "SETTLED") echo "SETTLED";;
  "OPEN") echo "OPEN";;
  *) echo "Error"
esac

## Logging
echo "####END CheckInvoice" >> $var_logPath
