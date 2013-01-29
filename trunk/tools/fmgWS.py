#--------------------------------------------------------------------------------------
# this file can be imported in a python script in order to access the FMG web Services
# Note that the FMG's interface must have allow Web services access
# check your FMG configuration on GUI or CLI
# Python Package suds is needed
# Authors: - jrlabarriere@fortinet.com
#       
# Thanks to suds package, it rocks !!!!!  
#
# Not all requests defined in FMG Web Services are implemented in this fmgWS class
# For instance all requests used to manage/update FortiClient are not implemented as
# FMG will not support Forticlient FMG in 5.0 version
# this classe has been tested on post 4.3.7 FMG version B689. 
#--------------------------------------------------------------------------------------
import string
try:
	from suds.client import Client
	import logging
	from datetime import datetime
except ImportError:
	print 'package suds must be installed in order to use this fmgWS class, please install version 0.3.9 or higher, exiting now ....'
	exit()
	
class fmgWS:
	""" FortiManager Class allowing to perform  requests calls to the FortiManager device thru WebServices"""
	_spin=None
	_sphd=None
	_Jah=None
	_wshelp={}
	def __init__(self,fmgip,user,passw,verbose=0,debug=0):
		try:
			url='https://' + fmgip + ':8080/'
			_Jah=Client(url)
			sphd=_Jah.factory.create('servicePass')
			sphd.userID='?'
			sphd.password='?'
			self.sphd=sphd
			_Jah.set_options(soapheaders=sphd)
			spin=_Jah.factory.create('servicePass')
			spin.userID=user
			spin.password=passw
			self._Jah=_Jah
			self.spin=spin
			self._fill_help()
			logging.basicConfig(level=logging.INFO)
			if debug:
				logging.getLogger('suds.client').setLevel(logging.DEBUG)
				logging.getLogger('suds.transport').setLevel(logging.DEBUG)
			if verbose:
				print 
				print "Yop Man !, type <yourobject>.help() for command syntax "
				print 
		except Exception, e:
			print 'Error from class :',type(e)
			print e
			exit()
	
	def objectFactory(self, name):
		""" Instanciate an object of type given by name and return it """
		try:
			obj=self._Jah.factory.create(name)
			return obj
		except Exception, e:
			print type(e)
			print e

	def setDebug(self):
		"""use to display debug info on SOAP message processing at package's client and transport level"""
		logging.getLogger('suds.client').setLevel(logging.DEBUG)
		logging.getLogger('suds.transport').setLevel(logging.DEBUG)

	def unsetDebug(self):
		""" Unset the output of debugging information at package's client and transport level"""
		logging.getLogger('suds.client').setLevel(logging.INFO)
		logging.getLogger('suds.transport').setLevel(logging.INFO)
	
	def _serviceFactory(self,name):
		""" Instanciate the method given by name """
		try:
			service=self._Jah.service(name)
			return service
		except Exception, e:
			print type(e)
			print e
		
	def getDeviceList(self,adomName,detail):
		""" get the device list from the specified adom name , return an getDeviceListResponse instance or Error """
		try:
			result=self.objectFactory('getDeviceListResponse')
			result=self._Jah.service.getDeviceList(self.spin,adomName,detail)
			return result
		except Exception, e:
			print type(e)
			print e

	def getDeviceLicenseList(self):
		""" shows Device licence information """
		try:
			result=self.objectFactory('getDeviceLicenseListResponse')
			result=self._Jah.service.getDeviceLicenseList(self.spin)
			return result
		except Exception, e:
			print type(e)
			print e

			
	def getGroupList(self,adomName,detail=1):
		""" get the group list from the specified adom name, return an getGroupListResponse instance or Error """
		try:
			result=self.objectFactory('getGroupListResponse')
			result=self._Jah.service.getGroupList(self.spin,adomName,detail)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def getPackageList(self,adomName):
		""" get Policy Packages list from the specified Adom, if successful return a getAdomListResponse or error """
		try:
			result=self.objectFactory('getPackageListResponse')
			result=self._Jah.service.getPackageList(self.spin,adomName)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def getAdomList(self):
		""" get the list of ADOM defined in the FMG device , return an getAdomListResponse instance or Error"""
		try:
			result=self.objectFactory('getAdomListResponse')
			result=self._Jah.service.getAdomList(self.spin)
			return result
		except Exception, e:
			print type(e)
			print e

	def getDeviceLicenseList(self):
		""" get the list of license information foor all fgt devices, return an getDeviceLicenseListResponse instance or Error"""
		try:
			result=self.objectFactory('getDeviceLicenseListResponse')
			result=self._Jah.service.getDeviceLicenseList(self.spin)
			return result
		except Exception, e:
			print type(e)
			print e

			
	def addAdom(self,name,version,mr,isBackupMode=0,VPNManagement=0,devSNVdom=[],devIDVdom=[]):
		""" add an adom and members like device or vdom """
		try:
			result=self.objectFactory('addAdomResponse')
			result=self._Jah.service.addAdom(self.spin,name,version,mr,isBackupMode,VPNManagement,devSNVdom,devIDVdom)
			return result
		except Exception, e:
			print type(e)
			print e

	def editAdom(self,name,version,mr,state,isBackupMode=0,VPNManagement=0,metafields=None,devSNVdom=[],devIDVdom=[]):
		""" edit an adom and members like device or vdom """
		try:
			result=self.objectFactory('editAdomResponse')
			result=self._Jah.service.editAdom(self.spin,name,version,mr,state,isBackupMode,VPNManagement,metafields,devSNVdom,devIDVdom)
			return result
		except Exception, e:
			print type(e)
			print e
				
	def deleteAdom(self,adom,adomOid):
		""" delete the adom, name and Oid are required """
		try:
			result=self.objectFactory('deleteAdomResponse')
			result=self._Jah.service.deleteAdom(self.spin,adom,adomOid)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def getDeviceVdomList(self,devName,devId):
		""" get device list of Vdoms, return a list of getDeviceVdomListResponse items """
		try:
			result=self.objectFactory('getDeviceVdomListResponse')
			result=self._Jah.service.getDeviceVdomList(self.spin,devName,devId)
			return result
		except Exception, e:
			print type(e)
			print e
			
	def addDevice(self, adom, ip, autod, deviceType, devName, adminUser, password, version, mr,model, flags, descrip, devId):
		""" Add a device in FMG , return an addDeviceResponse instance or Error """
		try:
			result=self.objectFactory('addDeviceResponse')
			result=self._Jah.service.addDevice(self.spin,adom,ip,autod,deviceType,devName, adminUser,password,version,mr,model, flags,descrip,devId)
			return result
		except Exception, e:
			print type(e)
			print e
		
	def getDevices(self,snbs=[],ids=[]):
		try:
			#lsn=[]
			#lids=[]
			#if len(sn)>0:
			#	lsn=snbs.split(',')
			#if len(ids)>0:
			#	lids=ids.split(',')
			result=self.objectFactory('getDevicesResponse')
			result=self._Jah.service.getDevices(self.spin,snbs,ids)
			return result
		except Exception, e:
			print type(e)
			print e

	def deleteDevice(self,devId,sn=''):
		""" delete the given device from FMG managed devices, return deleteDeviceResponse instance or error """
		try:
			result=self.objectFactory('deleteDeviceResponse')
			result=self._Jah.service.deleteDevice(self.spin,devId,sn)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def deleteConfigRev(self,devId,sn, revName, revId):
		""" delete the specified config revision from FortiManager, return deleteConfigRevResponse instance or error """ 
		try:
			result=self.objectFactory('deleteConfigRevResponse')
			result=self._Jah.service.deleteConfigRev(self.spin,devId,sn,revName,revId)
			return result
		except Exception, e:
			print type(e)
			print e

	def installConfig(self, sfrom, sto, adomName, pkgoid,devId, sn, newrevName):
		""" install configuration on a given managed device, return installConfigResponse instance or error"""
		# by default we force from policy package ( ADOM db)  to device 
		if sfrom=='':
			sfrom='global'
		if sto=='':
			sto=='remote'
		if (sfrom=='global') and (sto=='remote'):
			# heyhey force package install , whatever the parameters are
			devId=-1
			sn=''
		try:
			result=self.objectFactory('installConfigResponse')
			result=self._Jah.service.installConfig(self.spin,sfrom,sto,adomName,pkgoid,devId,sn,newrevName)
			return result
		except Exception, e:
			print type(e)
			print e
		
	def retrieveConfig(self,devId='',sn='',revname='fromWS'):
		""" retrieve a managed device's configuration into FMG database, return a retrieveConfigResponse instance or Error"""
		if sn=='' and devId=='':
			print 'missing parameters, enter devID or device serial number'
			return None
		else:
			try:
				result=self.objectFactory('retrieveConfigResponse')
				result=self._Jah.service.retrieveConfig(self.spin,devId,sn,revname)
				return result
			except Exception, e:
				print type(e)
				print e
				
	def getInstlog(self,devID,sn='',taskId=1):
		""" retrieve log information for a given task known by taskId, return a getInstLogResponse instance or Error """
		try:
			result=self.objectFactory('getInstlogResponse')
			result=self._Jah.service.getInstlog(self.spin,devID,sn,taskId)
		except Exception, e:
			print type(e)
			print e
				
	def revertConfig(self,devID,sn='',revID=1):
		""" revert the managed device configuration to the given revision Id, return a revertConfigResponse instance or Error"""
		if (sn=='' and devId=='') or revID==0:
			print 'missing parameters, enter devID or device serial number, and revID'
			return None
		else:
			try:
				result=self.objectFactory('revertConfigResponse')
				result=self._Jah.service.revertConfig(self.spin,devId,sn,revID)
				return result
			except Exception, e:
				print type(e)
				print e
							
	def getConfig(self,devId,serialNumber, adom,revNb=-1):
		""" get config fron a device specified by Serial Number or device Id , return a getConfigResponse instance or Error """
		try:
			result=self.objectFactory('getConfigResponse')
			result=self._Jah.service.getConfig(self.spin,devId,serialNumber,adom,revNb)
			return result
		except Exception, e:
			print type(e)
			print e

	def getConfigRevisionHistory(self,sn='',devID=0, checkinUser='', mincheckinDate=datetime(2001,01,01),maxcheckinDate=datetime(2023,12,31),minrevNB=0,maxrevNB=2000):
		""" get a revision history list for a given device, return a getConfigRevisionHistoryResponse instance or error """
		try:
			result=self.objectFactory('getConfigRevisionHistoryResponse')
			result=self._Jah.service.getConfigRevisionHistory(self.spin,sn,devID,checkinUser,mincheckinDate,maxcheckinDate,minrevNB,maxrevNB)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def listRevisionId(self,devId,sn='',revName=''):
		""" list RevisionID for a given device, return a listRevisionIdResponse instance or Error"""
		try:
			result=self.objectFactory('listRevisionIdResponse')
			result=self._Jah.service.listRevisionId(self.spin,devId,sn,revName)
			return result
		except Exception, e:
			print type(e)
			print e
			
				
	def createScript(self,adomname,scname,sctype='CLI',scdesc='from fmgWS',sccontent=' ',overwrit=1):
		""" create a script in FMG, return a createScriptREsponse instance or Error """
		try:
			result=self.objectFactory('createScriptResponse')
			result=self._Jah.service.createScript(self.spin,adomname,scname,sctype,scdesc,sccontent,overwrit)
			return result
		except Exception, e:
			print type(e)
			print e

	def runScript(self,scname,sctype,entId,sn,runonDB,pkgoid):
		""" run a stored script in FortiManager , return a runScriptResponse instance or Error """
		if sctype==None or sctype=='':
			sctype='CLI'
		try:
			result=self.objectFactory('runScriptResponse')
			result=self._Jah.service.runScript(self.spin,scname,sctype,entId,sn,runonDB,pkgoid)
			return result
		except Exception, e:
			print type(e)
			print e

	def deleteScript(self,name,type='CLI'):
		""" delete a Fortimanager script specified by name, return a deleteScriptResponse instance or Error """
		try:
			result=self.objectFactory('deleteScriptResponse')
			result=self._Jah.service.deleteScript(self.spin,name,type)
			return result
		except Exception, e:
			print type(e)
			print e


	def getScriptLogSummary(self,devId,sn='',maxlog=30):
		""" get a script Log summary from FMG on a specified device, return a getScriptLogSummaryResponse instance or Error """
		try:
			result=self.objectFactory('getScriptLogSummaryResponse')
			result=self._Jah.service.getScriptLogSummary(self.spin,devId,sn,maxlog)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def getScriptLog(self,devId,sn,logId,name):
		""" get the Script execution log on the specified device from Fortimanager, return a getScriptLog instance or Error"""
		try:
			result=self.objectFactory('getScriptLogResponse')
			result=self._Jah.service.getScriptLog(self.spin,devId,sn,logId,name)
			return result
		except Exception, e:
			print type(e)
			print e

	def getScript(self,name,typ='CLI'):
		""" get the script content specified by name from FMG , return a getScriptResponse instance or Error """  
		try:
			result=self.objectFactory('getScriptResponse')
			result=self._Jah.service.getScript(self.spin,name,typ)
			return result
		except Exception, e:
			print type(e)
			print e
	
	def getTaskList(self,adomName,taskId):
		""" get the subtasks list from Task defined by TaskId inside a Adom, return a getTaskListResponse or Error"""
		try:
			result=self.objectFactory('getTaskListResponse')
			result=self._Jah.service.getTaskList(self.spin,adomName,taskId)
			return result
		except Exception, e:
			print type(e)
			print e

	def _fill_help(self):
		""" create a detailed help from the fmgWS class and associated WSDL file ( internal to the instance """
		try:
		# let's dive in the definition , the real client is named _Jah ;-)
		# where are the ports ? services ? BTW self._Jah.wsdl contains the wsdl from fmg
		# but better to get methods from the marshalled objects , read the code of objects inherited
		# or just believe that the following code will run ! lol
			for sdef in self._Jah.sd:
				for port in sdef.ports:
					# normally FMG WS has only one service port but who knows !!!
					defs=port[1]
					# let's look at what it can do
					for met in defs:
						name=met[0]
						#print name
						params=met[1]
						#goal is to hide the servicePass object as it is already set
						ls=[]
						for i in range(1,len(params)):
							st=sdef.xlate(params[i][1]).split(':')
							if len(st) > 1:
								st=st[1]
							else:
								st=sdef.xlate(params[i][1])
							par= "%s %s" % (st,params[i][0])
							#print par
							ls.append(par)
						self._wshelp[name]=ls
		except Exception, e:
			print type(e)
			print e
			exit()
	
	def help(self,hkey=None):
		""" provide a method description for this instance, parameter string entered is used to search for a specific method """
		lkey=[]
		if (hkey==None) or  not (isinstance(hkey,str)):
			tmpkey=sorted(self._wshelp.keys())
			for k in tmpkey:
				if ((string.find(k.upper(),'FCT')==-1) and (string.find(k.upper(),'TCL')==-1)) :
					lkey.append(k)
		else:
			stt=hkey.upper()
			for k in sorted(self._wshelp.keys()):
				if (string.find(k.upper(),stt)> -1) and (string.find(k.upper(),'FCT')== -1):
					lkey.append(k)
		for k in lkey:
			#print k
			if (string.find(k.upper(),'TCL')) > -1:
				l='( TCL is not a snake specie like python, this method is not implemented !!! ) \n '
			else:
				l='('
				for it in self._wshelp[k]: 
					l=l+it+', ' # not nice better to use join !!!!
				if len(l)>2:
					l=l[:len(l)-2]
				l=l+')\n'
			print k+l
