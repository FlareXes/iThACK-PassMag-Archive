from Password_Manager.User._db_manager import dump_all_tables
from Password_Manager.User._data_encryption import decryptPassword
from Password_Manager._Authenticate import checkTrust
from pandas import DataFrame

def export_tocsv(export_location: str) -> None:
    # Authenticate
    masterPassword = checkTrust()

    # Dump Database Tables
    dump_tables = dump_all_tables()
    item_info, encryption_components_list = dump_tables[0], dump_tables[1]

    ExportEntries = []
    for i in range(0, len(encryption_components_list)):
        encryption_components = item_info[i][5] + encryption_components_list[i][0]
        cipher_text = encryption_components[:-168]
        salt = encryption_components[-168:-48]
        nonce = encryption_components[-48:-24]
        tag = encryption_components[-24:]

        decryptedPassword = decryptPassword(cipher_text, salt, nonce, tag, masterPassword).decode('utf-8')
        rowList = list(item_info[i])
        rowList[5] = decryptedPassword
        ExportEntries.append(tuple(rowList))

    df = DataFrame(ExportEntries, columns=["ID", "Website", "URL", "Username", "Email", "Password", "Description"])
    df.to_csv(f"{export_location}/iThACK-PassMag-export.csv", index=False)