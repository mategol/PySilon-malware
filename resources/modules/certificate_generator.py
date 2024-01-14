from OpenSSL import crypto, SSL

#'signtool sign /f "certificate.pfx" /tr "http://timestamp.digicert.com" /td SHA256 /fd SHA256 "test.exe"'

def cert_gen(
    emailAddress="",
    commonName="",
    countryName="NT",
    localityName="",
    stateOrProvinceName="",
    organizationName="",
    organizationUnitName="",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    KEY_FILE = "private.key",
    CERT_FILE="selfsigned.crt",
    PFX_FILE="certificate.pfx"):

    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.get_subject().emailAddress = emailAddress
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(validityStartInSeconds)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    with open(KEY_FILE, "wt") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode('utf-8'))
    with open(CERT_FILE, "wt") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8'))

    pfx = crypto.PKCS12()
    pfx.set_privatekey(k)
    pfx.set_certificate(cert)
    with open(PFX_FILE, "wb") as pfx_file:
        pfx_file.write(pfx.export())

cert_gen()