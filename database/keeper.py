import sys, os
temp = os.path.abspath(os.pardir) + '\\temp\\'

import pickle
import hashlib

class Keeper:

	def __init__(self, fname):
		self.fname = os.path.abspath(os.pardir) + '\keeper.db'
		self.files = {'cfilepath': temp + 'temp1234.rybdb',
						'pwfile': temp + 'temp1234_pw.rybdb',
						'markerfile': False,
						'dbpw': self.hashpw("Quel'danas2007"),
						'resetpw': True}
		
		if os.path.exists(self.fname):
			self.load()
		else:
			self.fname = os.path.abspath(os.pardir) + '\keeper.db'
			self.save()

	def hashpw(self, pw):
		md5_hasher = hashlib.md5()
		md5_hasher.update(str.encode(pw))
		return md5_hasher.digest()

	def load(self):
		self.files = pickle.load(open(self.fname, "rb"))
		if not os.path.exists(self.files['cfilepath']) or \
			not os.path.exists(self.files['pwfile']):
			self.files['cfilepath'] = temp + 'temp1234.rybdb'
			self.files['pwfile'] = temp + 'temp1234_pw.rybdb'
			self.save()

	def save(self):
		pickle.dump(self.files, open(self.fname, "wb"))