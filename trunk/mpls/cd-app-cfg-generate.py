#!/usr/bin/python


import os, sys, time
from devicecontrol import DC
class mpls_ce_app():
    def __init__ (self):
        self.FGT_Left = "10.10.0.16"
        self.FGT_Left_Username = "admin"
        self.FGT_Left_Password = ""
        self.Debug = 5
        self.FGT_Left_Cli = []
        self.FGT_Left_ClientInterface = "port9"
        self.FGT_Left_ServerInterface = "port7"

        
    def GenVdom (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit c_"+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenVlan(self,i=1):
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ClientInterface + "_c_" +str(i))
        self.FGT_Left_Cli.append ("set ip 10.1."+str(i)+".1/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh  telnet")
        self.FGT_Left_Cli.append ("set vdom c_"+str(i))
        self.FGT_Left_Cli.append ("set inter "+self.FGT_Left_ClientInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i+1000))
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("end")
        
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ServerInterface + "_c_" + str(i))
        self.FGT_Left_Cli.append ("set ip 10.2."+str(i)+".1/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh telnet")
        self.FGT_Left_Cli.append ("set vdom c_"+str(i))
        self.FGT_Left_Cli.append ("set inter "+self.FGT_Left_ServerInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i+1000))
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("end")
        return 0

    def GenBGPRouting (self,i=1) :
        self.FGT_Left_Cli.append ("config vdom")
        self.FGT_Left_Cli.append   ("edit c_"+str(i))
        self.FGT_Left_Cli.append ("config router bgp")
        self.FGT_Left_Cli.append   ("set as "+str(i))
        self.FGT_Left_Cli.append   ("config neighbor")
        self.FGT_Left_Cli.append     ("edit 10.1."+str(i) +".254")
        self.FGT_Left_Cli.append       ("set remote-as 4000")
        self.FGT_Left_Cli.append     ("end")
        self.FGT_Left_Cli.append   ("set router-id 10.1."+str(i)+".1")
        self.FGT_Left_Cli.append   ("config network")
        self.FGT_Left_Cli.append   ("edit 0")
        self.FGT_Left_Cli.append     ("set prefix 10.2."+str(i) +".0 255.255.255.0")
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append   ('config redistribute "connected"')
        self.FGT_Left_Cli.append    ("set status enable")
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append   ('config redistribute "static"')
        self.FGT_Left_Cli.append    ("set status enable")
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Left_Cli.append ("end") #leave vdom
        return 0

    def GenStaticRoute (self,i=1):
        # config static route for ssl-vpn tunnel address
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append    ("edit c_"+str(i))
        self.FGT_Left_Cli.append  ("config router static")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append    ("set dst 0.0.0.0")
        self.FGT_Left_Cli.append    ("set gateway 10.2."+str(i)+".254")
        self.FGT_Left_Cli.append    ("set device "+self.FGT_Left_ServerInterface+"_c_"+ str(i))
        self.FGT_Left_Cli.append   ("end")     #Leave Static Route mode
        self.FGT_Left_Cli.append  ("end")     #Leave vdom v[N]
        return 0
    
    
    def GenFWPolicy (self,i=1):
        # This policy is for web-mode ssl vpn 
        self.FGT_Left_Cli.append ("config vdom")
        self.FGT_Left_Cli.append   ("edit c_"+str(i))
        self.FGT_Left_Cli.append ("config fire policy")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append   ('set srcintf '+self.FGT_Left_ClientInterface+"_c_"+str(i))
        self.FGT_Left_Cli.append   ('set dstintf '+self.FGT_Left_ServerInterface+"_c_"+str(i))
        self.FGT_Left_Cli.append   ('set srcaddr "all"')
        self.FGT_Left_Cli.append   ('set dstaddr "all"')
        self.FGT_Left_Cli.append    ('set service "ANY"')
        self.FGT_Left_Cli.append    ('set schedule "always"')
        self.FGT_Left_Cli.append   ("set action accept")
        self.FGT_Left_Cli.append  ("next")
        
        # This policy for tunnel mode ssl_vpn traffic
        self.FGT_Left_Cli.append   ("edit 0")
        self.FGT_Left_Cli.append    ('set dstintf '+self.FGT_Left_ClientInterface+"_c_"+str(i))
        self.FGT_Left_Cli.append    ('set srcintf '+self.FGT_Left_ServerInterface+"_c_"+str(i))
        self.FGT_Left_Cli.append    ('set srcaddr "all"')
        self.FGT_Left_Cli.append    ('set dstaddr "all"')
        self.FGT_Left_Cli.append    ("set action accept")
        self.FGT_Left_Cli.append    ('set schedule "always"')
        self.FGT_Left_Cli.append    ('set service "ANY"')
        self.FGT_Left_Cli.append    ('set logtraffic disable')
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenLocalUser (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit v"+str(i))
        self.FGT_Left_Cli.append  ("config user local")
        self.FGT_Left_Cli.append  ('edit qa')
        self.FGT_Left_Cli.append  ("set type password")
        self.FGT_Left_Cli.append ("set passwd qa1234")
        self.FGT_Left_Cli.append  ("end")
        # Below is user-group link to ssl-vpn
        self.FGT_Left_Cli.append  ("config user group")
        self.FGT_Left_Cli.append  ("edit ssl")
        self.FGT_Left_Cli.append ("set group-type sslvpn")
        self.FGT_Left_Cli.append  ("set member qa")
        self.FGT_Left_Cli.append  ("set sslvpn-portal "+"v_"+str(i))
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Left_Cli.append ("end") #leave vdom
        return 0

    def GenAll (self,i):
        self.FGT_Left_Cli = []
        self.GenVdom(i)
        self.GenVlan(i)
        self.GenStaticRoute(i)
        self.GenBGPRouting (i)
#        self.GenStaticRoute (i)
#        self.GenSSLVPNSetting(i)
#        self.GenLocalUser(i)
        self.GenFWPolicy(i)


if __name__ == '__main__' :
    a = mpls_ce_app ()
    fgt_left    = DC (a.FGT_Left,  "fgt")
    #fgt_left.SetDebugLevel()

    #fgt_right.SetDebugLevel()
    #fgt_left.DCTelnetDevice_FGT ()

    #print "left ", fgt_left.Err
    #fgt_right.DCTelnetDevice_FGT ()
    #print "right", fgt_right.Err 
    print "config global"
    print "exec batch start"
    for i in range (1 ,11) :
        a.GenAll(i)
        print "#" * 10, "Generate Config for FGT Vdom --" , i
        for i in a.FGT_Left_Cli[:] : print i
        #fgt_left.DCUploadCFG_FGT (a.FGT_Left_Cli)
        #print '=' * 70
        #for i in range(len(a.FGT_Left_Cli)) :
        #    print a.FGT_Left_Cli[int(i)]
        #print '=' * 70
        #for i in range (len(a.FGT_Right_Cli)) :
        #    print a.FGT_Right_Cli[int(i)]
        #fgt_left.DCUploadCFG_FGT(a.FGT_Left_Cli)
#    a.GenAll(11)
    print "exec batch end"


