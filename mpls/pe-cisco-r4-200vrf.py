#!/usr/bin/python

# *Generate configure for R3, R4
# *Generate VRF for each MPLS-VPN CE
# *Generate Router Interface : bind VRF to interface 
# *Generate BGP VRF

import os, sys, time
from devicecontrol import DC
class mpls_pe_app():
    def __init__ (self):
        self.FGT_Left = "10.10.10.4"
        #self.FGT_Left = "10.10.10.5"
        self.FGT_Left_Username = "admin"
        self.FGT_Left_Password = ""
        self.Debug = 5
        self.FGT_Left_Cli = []
        self.FGT_Left_ClientInterface = "port4"
        self.FGT_Left_ServerInterface = "port10"
    def SetDeviceLeftMGMTIP (self, IP):
        self.FGT_Left = IP

    def GenVdom (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit c_"+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenLoopback(self,i=1):
        self.FGT_Left_Cli.append ("config t")
        self.FGT_Left_Cli.append ("inter loop "+str(i))
        self.FGT_Left_Cli.append ("ip vrf forw vrf-c"+str(i))
        #Below is for R4 PE-CE vrf
        self.FGT_Left_Cli.append ("ip add 10.4."+str(i)+".2 255.255.255.255")
        
        #Below is for R5 PE-CE vrf
        #self.FGT_Left_Cli.append ("ip add 10.5."+str(i)+".2 255.255.255.255")
        self.FGT_Left_Cli.append ("end")
        return 0

    def GenBGPRouting (self,i=1) :
        self.FGT_Left_Cli.append ("config router bgp")
        self.FGT_Left_Cli.append   ("set as "+str(i))
        self.FGT_Left_Cli.append   ("config neighbor")
        self.FGT_Left_Cli.append     ("edit 10.1."+str(i) +".1")
        self.FGT_Left_Cli.append       ("set remote-as "+str(i))
        self.FGT_Left_Cli.append     ("end")
        self.FGT_Left_Cli.append   ("set router-id 10.1."+str(i)+".1")
        self.FGT_Left_Cli.append  ("end")
        return 0

    def GenBGPVRFRouting (self,i=1):
        # 
        self.FGT_Left_Cli.append  ("config t")
        self.FGT_Left_Cli.append    ("router bgp 4000")
        self.FGT_Left_Cli.append    ("address ipv4 vrf vrf-c"+str(i))
        self.FGT_Left_Cli.append      ("redistr connect")
        self.FGT_Left_Cli.append      ("redistr static")
        self.FGT_Left_Cli.append    ("exit")
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
        self.FGT_Left_Cli.append  ("conf t")
        self.FGT_Left_Cli.append  ("ip vrf vrf-c"+str(i))
        self.FGT_Left_Cli.append  ('rd 1:'+str (i))
        self.FGT_Left_Cli.append  ('route-target both 1:'+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0

    def GenAll (self,i):
        self.FGT_Left_Cli = []
#       self.GenVdom(i)
        self.GenVRF (i)
        self.GenLoopback(i)
        #self.GenRouterInterface(i)
        self.GenBGPVRFRouting (i)
#        self.GenStaticRoute (i)
#        self.GenSSLVPNSetting(i)
#        self.GenLocalUser(i)
#        self.GenFWPolicy(i)


if __name__ == '__main__' :
    a = mpls_pe_app ()
    a.SetDeviceLeftMGMTIP ("10.10.10.4")  # set Device IP 
    #a.SetDeviceLeftMGMTIP ("10.10.10.5")  # set Device IP 
    fgt_left = DC (a.FGT_Left,  "cisco_router")
    fgt_left.SetDebugLevel(0)

    fgt_left.DCTelnetDevice_Router ()

    print "left ", type (fgt_left), fgt_left.Err
    #fgt_right.DCTelnetDevice_FGT ()
    #print "right", fgt_right.Err 

    for i in range (1 ,201) :
        a.GenAll(i)
        print "#" * 10, "Generate Config for Router: VRF -- " , i
        #for i in a.FGT_Left_Cli[:] : print i
        fgt_left.DCUploadCFG_Router (a.FGT_Left_Cli)
        #print '=' * 70
        #for i in range(len(a.FGT_Left_Cli)) :
        #    print a.FGT_Left_Cli[int(i)]
        #print '=' * 70
        #for i in range (len(a.FGT_Right_Cli)) :
        #    print a.FGT_Right_Cli[int(i)]
        #fgt_left.DCUploadCFG_FGT(a.FGT_Left_Cli)
#    a.GenAll(11)



