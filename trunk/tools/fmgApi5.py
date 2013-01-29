# Thanks to Steve Ding for this
# jr
import string
import json
import urllib
import urllib2

class fmgApi5:
        """ FortiManager Class allowing to perform methods calls to the FortiManager device thru JSON"""
        _httpheaders=None
        __url=None
        __session=None
        __saveinfile=None
                                
        def __init__(self,fmgip,uname='admin',passwd='',secure=0):
                _url='http://'
                if secure:
                        _url='https://'
                self.__url=_url+fmgip+'/jsonrpc'
                self._httpheaders={"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}
                self.__session=self._login(uname,passwd)
                if self.__session == None:
                        print "Login session fail."
                        exit
                else:
                        print "Login session successfully."
                                        
                                
        def _pack_obj_request(self,obj):
                req='{'
                for o in obj:
                        req=req+o+','
                req=req[:len(req)-1]
                req=req+'}'
                return req

        def _pack_lst_request(self,lst):
                req='['
                for l in lst:
                        req=req+l+','
                req=req[:len(req)-1]
                req=req+']'
                return req

        def _pack_key_val(self,key,val):
                str1=''
                if val==None:
                        str1='"'+key+'" : null'
                        return str1 
                if isinstance(val,int) or isinstance(val,long):
                        val=str(val)
                        str1='"'+key+'" : '+ val
                        return str1
                str1='"'+key+'" : "'+val+'"'
                return str1

        def _concat_param(self,l1,l2):
                str1=''
                str1='"'+l1+ '" : '+ l2 
                return str1

        def _login(self,usrname,passwd,sid=1,url='sys/login/user'):

                par1=self._pack_key_val('url',url)
                u1=self._pack_key_val('user',usrname)
                u2=self._pack_key_val('passwd',passwd)
                u3=u1+','+u2
                d1=self._pack_obj_request((u3,))
                d2=self._pack_lst_request((d1,))
                d3=self._concat_param('data',d2)
                par1=par1+','+d3
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','exec')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                msg=self._pack_obj_request((line1,line2,line3))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                if obj['result']['status']['code'] == 0 and obj['result']['status']['message'] == 'OK':
                        return obj['session']
                else:
                        return None

        def _logout(self,sid=1,url='sys/logout'):

                par1=self._pack_key_val('url',url)
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','exec')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',self.__session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                if obj['result']['status']['code'] == 0 and obj['result']['status']['message'] == 'OK':
                        return 1
                else:
                        return 0

        def _read(self,url,sid,session,additional):

                par1=self._pack_key_val('url',url)
                if additional != None:
                        par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','get')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _write(self,url,sid,session,data):

                par1=self._pack_key_val('url',url)
                par_d=self._concat_param('data',data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','set')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _add(self,url,sid,session,data):

                par1=self._pack_key_val('url',url)
                par_d=self._concat_param('data',data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','add')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _update(self,url,sid,session,data):

                par1=self._pack_key_val('url',url)
                par_d=self._concat_param('data',data)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','update')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _delete(self,url,sid,session,additional):

                par1=self._pack_key_val('url',url)
                if additional != None:
                        par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','delete')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _pkg_read(self,url,sid,session,additional):

                par1=self._pack_key_val('url',url)
                if additional != None:
                        par1=par1+','+additional
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','get')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj

        def _pkg_write(self,url,sid,session,children,name):

                par1=self._pack_key_val('url',url)
                if name != None:
                        n1=self._pack_key_val('name',name)
                        par1=par1+','+n1
                par_d=self._concat_param('children',children)
                par1=par1+','+par_d
                par2=self._pack_obj_request((par1,))
                par3=self._pack_lst_request((par2,))
                line1=self._pack_key_val('method','set')
                line2=self._concat_param('params',par3)
                line3=self._pack_key_val('id',sid)
                line4=self._pack_key_val('session',session)
                msg=self._pack_obj_request((line1,line2,line3,line4))
                #print msg
                #print
                myreq=urllib2.Request(self.__url,msg,self._httpheaders)
                handler=urllib2.urlopen(myreq)
                res=''   
                res= handler.read()
                #print res
                #print
                obj=json.loads(res)
                return obj


        def execute(self,data):
                
                if data['method']=='get':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        if data.has_key('additional'):
                           additional=data['additional']
                        else:
                           additional=None;
                        obj=self._read(prefix+url,int(sid),self.__session,additional)
                        if obj.has_key('id') and str(obj['id']) == sid:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == prefix+url:
                                 if element.has_key('data') and element['data'] != None:
                                    return element['data']

                if data['method']=='set':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        dat=data['data']
                        obj=self._write(prefix+url,int(sid),self.__session,dat)
                        if obj.has_key('id') and str(obj['id']) == sid:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == prefix+url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']


                if data['method']=='add':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        dat=data['data']
                        obj=self._add(prefix+url,int(sid),self.__session,dat)
                        if obj.has_key('id') and str(obj['id']) == sid:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == prefix+url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']


                if data['method']=='update':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        dat=data['data']
                        obj=self._update(prefix+url,int(sid),self.__session,dat)
                        if obj.has_key('id') and str(obj['id']) == sid:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == prefix+url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']
                                        

                if data['method']=='delete':
                        prefix=data['prefix']
                        url=data['url']
                        sid=data['sid']
                        if data.has_key('additional'):
                           additional=data['additional']
                        else:
                           additional=None;
                        obj=self._delete(prefix+url,int(sid),self.__session,additional)
                        if obj.has_key('id') and str(obj['id']) == sid:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == prefix+url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']


                       
        def tear(self):

            re=self._logout()
            if re==1:
               print "Logout session successfully."
            if re==0:
               print "Logout session failed."

            

        def read(self,url,opt):

            if isinstance(opt,list) or isinstance(opt,dict):
                    opt=json.dumps(opt)
                    opt=opt.replace('{','')
                    opt=opt.replace('}','')
                    obj=self._read(url,1,self.__session,opt)
            else:
                    obj=self._read(url,1,self.__session,opt)                
            
            if obj.has_key('id') and obj['id'] == 1:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == url:
                                 if element.has_key('data') and element['data'] != None:
                                    return element['data']
            

        def write(self,url,data):
                
            if isinstance(data,list) or isinstance(data,dict):
                    data=json.dumps(data)
                    obj=self._write(url,1,self.__session,data)
            else:
                    obj=self._write(url,1,self.__session,data)
                    
            if obj.has_key('id') and obj['id'] == 1:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']


        def add(self,url,data):
                
            if isinstance(data,list) or isinstance(data,dict):
                    data=json.dumps(data)
                    obj=self._add(url,1,self.__session,data)
            else:
                    obj=self._add(url,1,self.__session,data)
                    
            if obj.has_key('id') and obj['id'] == 1:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status'], element['data']
                                

        def update(self,url,opt):
                
            if isinstance(data,list) or isinstance(data,dict):
                    data=json.dumps(data)
                    obj=self._update(url,1,self.__session,data)
            else:
                    obj=self._update(url,1,self.__session,data)
                    
            if obj.has_key('id') and obj['id'] == 1:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']
                                

        def delete(self,url,opt):
                
             if isinstance(opt,list) or isinstance(opt,dict):
                    opt=json.dumps(opt)
                    opt=opt.replace('{','')
                    opt=opt.replace('}','')
                    obj=self._delete(url,1,self.__session,opt)
             else:
                    obj=self._delete(url,1,self.__session,opt)

             if obj.has_key('id') and obj['id'] == 1:
                           for element in obj['result']:
                              if element.has_key('url') and element['url'] == url:
                                 if element.has_key('status') and element['status'] != None:
                                    return element['status']


	def saveRequests(self,filename):
		self.__saveinfile=filename
	
	def unsaveRequests(self):
		self.__saveinfile=None



									
	def __writefile(self,request,response):
		f=open(self.__saveinfile,'a')
		f.write('\n ---request--\n')
		json.dump(request,f,indent=4)
		f.write('\n ---response--\n')
		json.dump(response,f,indent=4)
		f.close()
				
									
									

	def sendPayload(self,input='payload.txt'):

		try:
			f=open(input,'r')
			data=f.read()
			f.close()
		except Exception as e:
			print 'error reading input json file ' + input
			print e
			return None
		try:
			obj1=json.loads(data)
		except Exception as e:
			print 'invalid json object defined in ' + input
			print e
			return None
		obj1['session']=self.__session
		req=json.dumps(obj1)
		myreq=urllib2.Request(self.__url,req,self._httpheaders)
		handler=urllib2.urlopen(myreq)
		s1=''	
		s1= handler.read()
		obj=json.loads(s1)
		if self.__saveinfile!=None:
			self.__writefile(json.loads(req),obj)
		#res=  obj['header']['result']
		return obj
			
	def sendPayloadstr(self,str):

		data=str
		try:
			obj1=json.loads(data)
		except Exception as e:
			print 'invalid json object defined in ' + input
			print e
			return None
		obj1['session']=self.__session
		req=json.dumps(obj1)
		myreq=urllib2.Request(self.__url,req,self._httpheaders)
		handler=urllib2.urlopen(myreq)
		s1=''	
		s1= handler.read()
		obj=json.loads(s1)
		if self.__saveinfile!=None:
			self.__writefile(json.loads(req),obj)
		#res=  obj['header']['result']
		return obj
                                        
