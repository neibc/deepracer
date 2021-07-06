#!/usr/bin/env python3

# pip install ecdsa
# pip install pysha3

# export ethereum account from google BigQuery open data
# SELECT `address`
# FROM `bigquery-public-data.crypto_ethereum.balances`
# WHERE `eth_balance` > 1
# ORDER BY `eth_balance` DESC
# LIMIT 4000000
# https://console.cloud.google.com/bigquery
#
# export it to ethacclist.csv

from ecdsa import SigningKey, SECP256k1
import sha3
import pandas as pd
import logging
import concurrent.futures

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

#def get_addr(priv_str, isprint=0):
def get_addr(priv_int, isprint=0):
#   priv_str = int("0000000000000000000000000000000000000000000000000000000000000001", 16).to_bytes(32, byteorder='big')
#   privinp = int(priv_str, 16).to_bytes(32, byteorder='big')
    privinp = priv_int.to_bytes(32, byteorder='big')
    priv = SigningKey.from_string(privinp, curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    addr = '0x' + keccak.hexdigest()[24:]

    if isprint!=0:
        print("Private key:", priv.to_string().hex())
        print("Public key: ", pub.hex())
        print("Address0:   ", addr)
        f = open('search_result.log','a')
        f.write('private_key:')
        f.write(priv.to_string().hex())
        f.write('\n')
        f.write('addr:')
        f.write(addr)
        f.write('\n')
    return addr

def example():
    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()

    keccak = sha3.keccak_256()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]

    print("Private key:", priv.to_string().hex())
    print("Public key: ", pub.hex())
    print("Address0:    ", address)
    print("Address:    ", checksum_encode(address))

    return

def test(addrstr):
    assert(addrstr == checksum_encode(addrstr))

def check_key(dict, key):
    ret = False
    if key in dict.keys():
        ret = True

    return ret
 
#example()
#get_addr("0000000000000000000000000000000000000000000000000000000000000001")
#get_addr("000000000000000000000000000000000000000000000000000000000000000a")
#get_addr("1111111111111111111111111111111111111111111111111111111111111111")
#get_addr("7777777777777777777777777777777777777777777777777777777777777777")
#get_addr("3141592653589793238462643383279502884197169399375105820974944592")
#get_addr("2718281828459045235362746639193200305992115738341879307021540551")
#get_addr("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

print('ethereum account search tool ver 0.1 by jskim')

startn = int("1000000000000000000000000000000000000000000000000000000001142560", 16)
endn = int("2000000000000000000000000000000000000000000000000000000000000001", 16)

print('start num:')
print(startn.to_bytes(32, byteorder='big').hex())
print('end num:')
print(endn.to_bytes(32, byteorder='big').hex())

logging.info('acc list file loading..')
dict_from_csv = pd.read_csv('ethacclist.csv', dtype={'address': object}).set_index('address').T.to_dict()
print('sample searching on the account list/richest one.. 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
print(check_key(dict_from_csv, '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'))

logging.info('start pair guessing..')

rangevar= range(startn, endn)

with concurrent.futures.ProcessPoolExecutor() as executor:
    for i, addr_str in zip(rangevar, executor.map(get_addr, rangevar)):
        if check_key(dict_from_csv, addr_str):
            print('BINGO:', addr_str)
            get_addr(i, 1)
        if i % 100000 == 0:
            logging.info(i.to_bytes(32, byteorder='big').hex())
            f = open('search_result.log','a')
            f.write(i.to_bytes(32, byteorder='big').hex())
            f.write('\n')
