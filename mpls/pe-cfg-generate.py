#!/usr/bin/python

# *Generate vlan which it can connect to CE-app FGT
# *Generate VRF for each MPLS-VPN CE
# *Generate Router Interface : bind VRF to interface 
# *Generate BGP VRF

import os, sys, time
from devicecontrol import DC
class mpls_pe_app():
    def __init__ (self):
        self.FGT_Left = "10.10.0.16"
        self.FGT_Left_Username = "admin"
        self.FGT_Left_Password = ""
        self.Debug = 5
        self.FGT_Left_Cli = []
        self.FGT_Left_ClientInterface = "port4"
        self.FGT_Left_ServerInterface = "port10"
        
    def GenVdom (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit c_"+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenVlan(self,i=1,option=2):
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ClientInterface + "_c_" +str(i))
        if (option == 1) :
            self.FGT_Left_Cli.append        ("set ip 10.1."+str(i)+".254/24")
        elif (option ==2) :
            self.FGT_Left_Cli.append ("set ip 10.1.1.254/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh  telnet")
        self.FGT_Left_Cli.append ("set vdom root")
        self.FGT_Left_Cli.append ("set inter "+self.FGT_Left_ClientInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i+1000))
        self.FGT_Left_Cli.append ("end")
        return 0

    def GenBGPRouting (self,i=1,option =1) :
        self.FGT_Left_Cli.append ("config router bgp")
        self.FGT_Left_Cli.append   ("set as "+str(i))
        self.FGT_Left_Cli.append   ("config neighbor")
        if (option == 2) :
            self.FGT_Left_Cli.append        ("edit 10.1."+str(i)+".1")
        elif (option ==1) :
            self.FGT_Left_Cli.append ("edit 10.1.1.1")
        self.FGT_Left_Cli.append       ("set remote-as "+str(i))
        self.FGT_Left_Cli.append     ("end")
        self.FGT_Left_Cli.append   ("set router-id 10.1."+str(i)+".1")
        self.FGT_Left_Cli.append  ("end")
        return 0

    def GenBGPVRFRouting (self,i=1,option=1):
        # 
        self.FGT_Left_Cli.append  ("config router bgp")
        self.FGT_Left_Cli.append    ("config vrf")
        self.FGT_Left_Cli.append    ("edit vrf-c"+str(i))
        self.FGT_Left_Cli.append      ("config neighbor")
        if (option == 1) :
            self.FGT_Left_Cli.append        ("edit 10.1."+str(i)+".1")
        elif (option ==2) :
            self.FGT_Left_Cli.append ("edit 10.1.1.1")
        self.FGT_Left_Cli.append          ("set remote-as "+str(i))
        self.FGT_Left_Cli.append      ("end")
        self.FGT_Left_Cli.append    ("end")
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    
    def GenRouterInterface (self,i=1):
        # This policy is for web-mode ssl vpn 
        self.FGT_Left_Cli.append ("config router interface")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ClientInterface + "_c_" +str(i))
        self.FGT_Left_Cli.append   ("set vrf vrf-c"+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenVRF (self,i=1):
        self.FGT_Left_Cli.append  ("config router vrf")
        self.FGT_Left_Cli.append  ("edit vrf-c"+str(i))
        self.FGT_Left_Cli.append  ('set descript "for Customer '+str (i)+ '"')
        self.FGT_Left_Cli.append  ('set rd 1:'+str(i))
        self.FGT_Left_Cli.append  ("config route-target ")
        self.FGT_Left_Cli.append   ("edit 1")
        self.FGT_Left_Cli.append     ("set import-export both")
        self.FGT_Left_Cli.append     ("set rt 1:"+str(i))
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append  ("end")
        return 0

    def GenAll (self,i):
        self.FGT_Left_Cli = []
#       self.GenVdom(i)
        self.GenVlan(i,2)
        self.GenVRF (i)
        self.GenRouterInterface(i)
        self.GenBGPVRFRouting (i,2)
#        self.GenStaticRoute (i)
#        self.GenSSLVPNSetting(i)
#        self.GenLocalUser(i)
#        self.GenFWPolicy(i)


if __name__ == '__main__' :
    a = mpls_pe_app ()
    fgt_left    = DC (a.FGT_Left,  "fgt")
    #fgt_left.SetDebugLevel()

    #fgt_right.SetDebugLevel()
    #fgt_left.DCTelnetDevice_FGT ()

    #print "left ", fgt_left.Err
    #fgt_right.DCTelnetDevice_FGT ()
    #print "right", fgt_right.Err 
    print "config global"
    print "exec batch start"
    for i in range (1 ,201) :
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


