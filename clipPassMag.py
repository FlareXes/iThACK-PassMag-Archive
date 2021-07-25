import time
import pyperclip
import subprocess
from Password_Manager._Authenticate import checkTrust
from Password_Manager.User._data_encryption import decryptPassword
from Password_Manager.User._db_manager import getColumn, getPasswordComponents

websites = getColumn('Website')
subprocess.check_output(['ipconfig', '/flushdns'], shell=False)
timeout = time.time() + 600  # 600 seconds
masterPassword = checkTrust()

try:
    while True:
        dnsLogs = str(subprocess.check_output(['ipconfig', '/displaydns'], shell=False))

        for website in websites:
            if website[1] in dnsLogs:
                encryptionComponents = getPasswordComponents(website[0])
                cipher_text = encryptionComponents[:-168]
                salt = encryptionComponents[-168:-48]
                nonce = encryptionComponents[-48:-24]
                tag = encryptionComponents[-24:]

                # Pattern should be (cipher_text, salt, nonce, tag, password)
                decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, masterPassword).decode('utf-8')
                pyperclip.copy(decryptedPassword)
                subprocess.check_output(['ipconfig', '/flushdns'], shell=False)

        if time.time() > timeout:
            pyperclip.copy('Time Up')
            break
except:
    quit()