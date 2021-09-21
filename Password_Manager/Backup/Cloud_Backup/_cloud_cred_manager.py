import json

def cloud_credential_setup():
    '''
    Setup cloud database credentials and then `iThACK PassMag` will manage that.
    '''
    try:
        print("\n1. DATABASE\n2. HOST\n3. PASSWORD\n4. USER")
        choose = input("\n⚠  If You Have These Credentials Then Continues (y/n): ")
        if choose == "y" or choose == "yes":
            while True:
                database = input("\nDatabases: ")
                host = input("Hosts: ")
                password = input("Password: ")
                user = input("User: ")
                print(f"\nDATABASE    >   {database}\nPASSWORD    >   {password}\nHOST        >   {host}\nUSER        >   {user}")

                confirm_choose = input("\n❗ Confirm Credentials - 'F' For Final Or 'E' For Edit: ")
                if confirm_choose == 'F' or confirm_choose == 'f':
                    cred_dict = {
                        "CleverCloud": {
                            "MYSQL_ADDON_DB": database,
                            "MYSQL_ADDON_HOST": host,
                            "MYSQL_ADDON_PASSWORD": password,
                            "MYSQL_ADDON_USER": user
                            }
                        }
                    with open("Password_Manager\Config\cloud_cred.json", "w", encoding ="utf-8") as file:
                        json.dump(cred_dict, file)
                    print("\n Successfully Completed ✌ 👌")
                    break
                else:
                    print("\nEdit Credentials Again 👇")
        else:
            print("❌ Process Canceled ❌")
            exit()
    except KeyboardInterrupt:
        print("\n\n❌ Process Interpreted ❌")