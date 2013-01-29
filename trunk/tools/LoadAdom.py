from fmgApi5 import *
from fmgWS import fmgWS
import string
import sys
from time import sleep


def submit_runScript(ws1,scname,ppoid):
	done=0
	while done < 1:
		try:
			ret=ws1.runScript(scname,'CLI',-1,'',1,ppoid)
			if ret != None:
				done=1
				return ret
		except Exception, e:
			print 'exception submit....'
			sleep(5)
			pass

def submit_createScript(ws1,adom,scname,scdesc,strf2,overw):			
	done=0
	while done < 1:
		try:
			ret=ws1.createScript(adom,scname,'CLI',scdesc,strf2,overw)
			if ret ==0:
				done=1
				return ret
		except Exception, e:
			print 'Exception 1......'
			sleep(5)
			pass
			
def getPackageList(ws1,adom):
	done=0
	while done < 1:
		try:
			ret=ws1.getPackageList(adom)
			if ret!=None:
				done=1
				return ret
		except Exception, e:
			print 'Exception 0....'
			sleep(5)
			pass

def wait_completion(ws1,adom,taskid):
	done=0
	while done < 1:
		print 'checking...'
		try:
			ret=ws1.getTaskList(adom,taskid)
			if ret != None:
				result=ret['taskList'][0]['deviceList'][0]['history']
				if len(result)>0:
					for r in result:
						if r['percentage']==100:
							done=1
			sleep(10)
		except Exception, e:
			print 'Exception wait.....'
			sleep(10)
			pass
			
			
		
if __name__ == '__main__':
	fmgip=raw_input('Enter FMG IP:')
	fmguser=raw_input('Enter Username: ')
	fmgpasw=raw_input('Enter password: ')
	payload='{"session": "", "params": [{"url": "pm/pkg/adom/$ADOM$", "data": [{"type": "pkg", "name": "$PPKG$"}]}], "method": "set", "id": 6}'
	targetadom=raw_input('Enter Adom name: ')
	mypayload=payload.replace('$ADOM$',targetadom)
	api=fmgApi5(fmgip,fmguser,fmgpasw)
	api.saveRequests('output.txt')
	for i in range(1,51):
		pp='PP-'+str(i)
		print 'creating policy package '+pp
		mypayload1=mypayload.replace('$PPKG$',pp)
		ret=api.sendPayloadstr(mypayload1)
	api.tear()
	sleep(5)
	print 'creating Web Service object.....'
	ws=fmgWS(fmgip,fmguser,fmgpasw)
	print 'getting Policy Packages list.....' 
	retPP=getPackageList(ws,targetadom)
	if  len(retPP)>0:
		PPoid=retPP[0]['oid']
		f=open('addr5000.cfg','r')
		strf=f.read()
		f.close()
		ret1=submit_createScript(ws,targetadom,'5000objects','5000 addr objects load',strf,1)
		f=open('fw5000pol.cfg','r')
		del strf
		strf1=f.read()
		f.close()
		ret1=submit_createScript(ws,targetadom,'5000fwrules','5000 fw rules ',strf1,1)
		print 'scripts created....'
		del strf1
		print 'running on oid ' + str(PPoid)
		sleep(5)
		sc_ret=submit_runScript(ws,'5000objects',PPoid)
		print 'loading objects......'
		print 'task id is ' + sc_ret['taskId']
		print 'checking completion....'
		taskid=sc_ret['taskId']
		wait_completion(ws,targetadom,taskid)
		print 'task id ' +taskid + ' done.....'
		print 'ready to load policies rules....'
		nb=len(retPP)
		print "found "+ str(nb)+" Policy Packages"
		i=0
		while i<nb:
			pp=retPP[i]
			if pp['name'] !='default':
				ppOID=pp['oid']
				try:
					sc_ret=submit_runScript(ws,'5000fwrules',ppOID)
					print 'task submitted for PP ' + pp['name']
					sleep(5)
					print 'checking completion....'
					taskid=sc_ret['taskId']
					wait_completion(ws,targetadom,taskid)
					i=i+1
				except Exception , err:
					print 'in exception1...'
					pass
			else:
				i=i+1
		print "job done...... I'm tired......"