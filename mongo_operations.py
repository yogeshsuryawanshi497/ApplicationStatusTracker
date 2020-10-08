'''
Script Name:	mongo_operations.py
Path:			\IPS_DecisionFabric\Control_Framework\
Description:	This module is considered as a module for the DF application
				and MongoDB transactions
Author:			Yogesh Suryawanshi
Revision History:
----------------------------------------------------------------------------------------------------------------------
S.No.			Date(MM/DD/YY)		Changed By			Change Description 	
----------------------------------------------------------------------------------------------------------------------
1.				05/27/2019			Y Suryawanshi		Initial Version (Exception Handling v1.1.1)
2.              06/18/2019          Shruti Joshi        SSL connection enabled       
3.              07/10/2019          Y Suryawanshi       standardized as per PEP8 standards
----------------------------------------------------------------------------------------------------------------------
'''
import sys
import pandas as pd
from pymongo import MongoClient
sys.path.insert(0,'/IPS_DecisionFabric/Form Processing')
import common_utils
import encryption_decryption
import pymongo
import ssl

class Mongo:
	"""successfully working"""
	def __init__(self):
		config_dict = common_utils.read_config_file()
		self.db_name = config_dict.get("db_name", "")
		self.db_uri = config_dict.get("db_uri", "")
		self.db_rs = config_dict.get("db_rs", "")
		self.db_user_name = config_dict.get("db_user_name", "")		
		self.db_ssl_flg = config_dict.get("db_ssl", "")				
		self.ssl_ca_certs_path = config_dict.get("ssl_ca_certs_path", "")
		self.ssl_certfile_path = config_dict.get("ssl_certfile_path", "")
		db_password = config_dict.get("db_password","")
		self.key = config_dict.get("key","")
		AESCipher_obj = encryption_decryption.AESCipher()
		db_password = AESCipher_obj.decrypt(db_password)
		self.db_password = db_password
		self.db_url = ('mongodb://{0}:{1}@{2}/{3}?replicaSet={4}'.format(self.db_user_name,
															  self.db_password,
															  self.db_uri,
															  self.db_name,
															  self.db_rs))
		
		if self.db_ssl_flg in [0,'0']:
			try:
				self.client = MongoClient(self.db_url,ssl=True,ssl_ca_certs=self.ssl_ca_certs_path, ssl_certfile=self.ssl_certfile_path,ssl_cert_reqs=ssl.CERT_NONE) 
				self.Mongodb = self.client[self.db_name]				
			except Exception as E:
				print("Unable to initiate mongodb instance : {}".format(E))
		else:
			try:
				self.client = MongoClient(self.db_url, ssl=True,ssl_ca_certs=self.ssl_ca_certs_path,ssl_certfile=self.ssl_certfile_path)
				self.Mongodb = self.client[self.db_name]				
			except Exception as E:
				print("Unable to initiate mongodb instance : {}".format(E))
				
	def insert_record_in_table(self, df, collection_name):
		"""successfully working"""
		try:
			cursor = self.Mongodb[collection_name]
			json_record = df.to_dict(orient='records')
			cursor.insert_many(json_record)
		except Exception as e:
			print("Unable to insert the record",e)

	def drop_table(self, collection_name):
		"""successfully working"""
		try:
			cursor = self.Mongodb[collection_name]
			cursor.drop()
			print("The table {} is dropped successfully"
				  "!".format(collection_name))
		except:
			print("Unable to drop the collection"
				  "{}".format(collection_name))


	def fetch_data_as_df(self, collection_name, query=None):
		cursor = self.Mongodb[collection_name].find(query)
		DF = pd.DataFrame(list(cursor))
		return DF
	def close(self):
		self.client.close()

def main():
	mongo = Mongo()
	db = mongo.Mongodb
	dict_type = []
	data = pd.DataFrame(list(db.DICT_VER_TRACKER.distinct("DictionaryType")))
	for i in data:
		print(i)
		dict_type.append(i)
	print(data)
	# for j in dict_type:
		# data1 = pd.DataFrame(list(db.DICT_VER_TRACKER.find({"DictionaryType": j,
															# "Action": "Export",
															# "Comment": "Exported by HRM"},
														   # {"FileName": 1, "DictionaryVersion": 1, "_id": 0}
														   # ).sort("Activity_DTM", pymongo.DESCENDING).limit(1)))
		# print(data1)

if __name__=="__main__":
	main()