# Protocol #
The mod\_ssl support three protocol SSLv2, SSLv3, TLSv1.
Configure Example:
```
#Turn on SSLv2 Only
SSLProtocol -all +SSLv2

#Turn off SSLv2
SSLProtocol all -SSLv2
#or
SSLProtocol SSLv3 TLSv1

```


# Cipher Suites #
The simply way to check all supported Cipher Suites:
```
openssl ciphers -v 

#or 
openssl ciphers -v 'EXP'

openssl ciphers -v 'SSLv3'

openssl ciphers -v 'TLSv1'
```