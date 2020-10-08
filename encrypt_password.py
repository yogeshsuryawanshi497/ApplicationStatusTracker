'''
Script Name:	encrypt_password.py
Path:			\IPS_DecisionFabric\Control Framework\
Description:	This is the calling script for encrypting the password provided as input. It calls the script 
				encryption_decryption.py for writing the encrypted password to config_file.txt
Author:			Harshita Rai
Revision History:
----------------------------------------------------------------------------------------------------------------------
S.No.			Date(MM/DD/YY)		Changed By			Change Description 	
----------------------------------------------------------------------------------------------------------------------
1.				07/16/2019			H Rai				Initial Version (IPS Decision Fabric v1.1.1)



----------------------------------------------------------------------------------------------------------------------

'''

if __name__ == '__main__':
	import encryption_decryption
	db_password = input('Please enter the password you want to Encrypt.')
	AESCipher_obj = encryption_decryption.AESCipher()
	edb_password = AESCipher_obj.encrypt(db_password)
	print("Encrypted DB password written to the config file. ")