import qrcode
import requests
import time
from pprint import pprint

from payment.payment_conf import (
    LNBITS_URL,
    LNBITS_INVOICE_API_KEY,
    SATS_PER_COCKTAIL
)


# only needed if paymentmethod uses invoices
def get_invoice(amount):
    url = '{LNBITS_URL}/payments'
    payload = {
        "out": False,
        "amount": amount,
        "memo": "cocktail"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": LNBITS_INVOICE_API_KEY
    }
    response = requests.request("POST", url, json=payload, headers=headers).json()
    return response


# only needed if paymentmethod uses invoices
def is_invoice_paid(payment_hash):
    url = f"{LNBITS_URL}/payments/{payment_hash}"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": LNBITS_INVOICE_API_KEY
    }
    response = requests.request("GET", url, headers=headers).json()
    return response


# only needed if paymentmethod uses invoices
def invoice_to_qr():
    response = get_invoice(SATS_PER_COCKTAIL)
    invoice = response["payment_request"]
    payment_hash = response["payment_hash"]
    img = qrcode.make(invoice)
    img.save('test_img.png')
    return payment_hash


# only needed if paymentmethod uses LNURL
def is_invoice_paid_2(old_balance):
    new_balance = get_balance()
    return new_balance >= (old_balance + SATS_PER_COCKTAIL)


# only needed if paymentmethod uses LNURL
def get_balance():
    url = f"{LNBITS_URL}/wallet"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": LNBITS_INVOICE_API_KEY
    }
    response = requests.request("GET", url, headers=headers).json()
    balance = response["balance"]
    return balance
