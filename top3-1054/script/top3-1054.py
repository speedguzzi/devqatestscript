#!/usr/bin/python


import os, sys, time
from devicecontrol import DC
class StressWAD ():
    def __init__ (self):
        self.FGT_Left = "10.10.0.44"
        self.FGT_Left_Username = "admin"
        self.FGT_Left_Password = ""
        self.Debug = 5
        self.FGT_Left_Cli = []
        self.FGT_Left_ClientInterface = "port1"
        self.FGT_Left_ServerInterface = "port2"

        
    def GenVdom (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit v"+str(i))
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenVlan(self,i=1):
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ClientInterface + "_v" +str(i))
        self.FGT_Left_Cli.append ("set ip 40.0."+str(i)+".1/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh  telnet")
        self.FGT_Left_Cli.append ("set vdom v"+str(i))
        self.FGT_Left_Cli.append ("set inter "+self.FGT_Left_ClientInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i))
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("end")
        
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit "+self.FGT_Left_ServerInterface + "_v" + str(i))
        self.FGT_Left_Cli.append ("set ip 30.0."+str(i)+".1/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh telnet")
        self.FGT_Left_Cli.append ("set vdom v"+str(i))
        self.FGT_Left_Cli.append ("set inter "+self.FGT_Left_ServerInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i))
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("end")
        return 0
    def GenSSLVPNSetting (self,i=1) :
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append   ("edit v"+str(i))
        self.FGT_Left_Cli.append ("config vpn ssl settings")
        self.FGT_Left_Cli.append   ("set sslv3 enable")
        self.FGT_Left_Cli.append   ("set sslvpn-enable enable")
        self.FGT_Left_Cli.append   ("set auth-timeout 28800")
        self.FGT_Left_Cli.append   ("set idle-timeout 300")
        self.FGT_Left_Cli.append   ("set reqclientcert disable")
        self.FGT_Left_Cli.append   ("set servercert self-sign")
        self.FGT_Left_Cli.append   ("set sslv2 disable")
        self.FGT_Left_Cli.append   ("set tunnel-endip 30.0." + str(i) + ".62")
        self.FGT_Left_Cli.append   ("set tunnel-startip 30.0." + str(i) + ".33")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("config vpn ssl web portal")
        self.FGT_Left_Cli.append  ("edit v_"+str(i))
        self.FGT_Left_Cli.append   ("set allow-access web ftp smb telnet ssh")
        self.FGT_Left_Cli.append   ("set page-layout double-column")
        self.FGT_Left_Cli.append  ("config widget")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append     ("set name Tunnel Mode")
        self.FGT_Left_Cli.append     ("set type tunnel")
        self.FGT_Left_Cli.append     ("set tunnel-status enable")
        self.FGT_Left_Cli.append    ("next")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append     ("set name Bookmarks")
        self.FGT_Left_Cli.append     ("set allow-apps web")
        self.FGT_Left_Cli.append    ("next")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append     ("set name Connection Tool")
        self.FGT_Left_Cli.append     ("set type tool")
        self.FGT_Left_Cli.append     ("set column two")
        self.FGT_Left_Cli.append     ("set allow-apps web ftp smb telnet ssh vnc rdp")
        self.FGT_Left_Cli.append    ("next")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append     ("set name Session Information")
        self.FGT_Left_Cli.append     ("set type info")
        self.FGT_Left_Cli.append     ("set column two")
        self.FGT_Left_Cli.append    ("next")
        self.FGT_Left_Cli.append  ("end") 
        self.FGT_Left_Cli.append ("end") 
        return 0

    def GenStaticRoute (self,i=1):
        # config static route for ssl-vpn tunnel address
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append    ("edit v"+str(i))
        self.FGT_Left_Cli.append  ("config router static")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append    ("set dst 30.0.1.32 "+"255 255.255.224")
        self.FGT_Left_Cli.append    ("set device "+self.FGT_Left_ServerInterface+"_v"+str(i))
        self.FGT_Left_Cli.append   ("end")     #Leave Static Route mode
        self.FGT_Left_Cli.append  ("end")     #Leave vdom v[N]
        return 0
    
    
    def GenFWPolicy (self,i=1):
        # This policy is for web-mode ssl vpn 
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("edit v"+str(i))
        self.FGT_Left_Cli.append ("config fire policy")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ('set srcintf '+self.FGT_Left_ClientInterface+"_v"+str(i))
        self.FGT_Left_Cli.append  ('set dstintf '+self.FGT_Left_ServerInterface+"_v"+str(i))
        self.FGT_Left_Cli.append  ('set srcaddr "all"')
        self.FGT_Left_Cli.append  ('set dstaddr "all"')
        self.FGT_Left_Cli.append  ("set action ssl-vpn")
        self.FGT_Left_Cli.append  ("config identity-based-policy")
        self.FGT_Left_Cli.append    ("edit 0")
        self.FGT_Left_Cli.append     ("set groups ssl")
        self.FGT_Left_Cli.append     ("set logtraffic disable")
        self.FGT_Left_Cli.append     ("set schedule always")
        self.FGT_Left_Cli.append     ("set service ANY")
        self.FGT_Left_Cli.append    ("next")
        self.FGT_Left_Cli.append   ("end")
        self.FGT_Left_Cli.append  ("next")
        
        # This policy for tunnel mode ssl_vpn traffic
        self.FGT_Left_Cli.append   ("edit 0")
        self.FGT_Left_Cli.append    ('set srcintf "ssl.v'+str(i))
        self.FGT_Left_Cli.append    ('set dstintf '+self.FGT_Left_ServerInterface+"_v"+str(i))
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
        return 0
    def GenAll (self,i):
        self.FGT_Left_Cli = []
        self.GenVdom(i)
        self.GenVlan(i)
        self.GenStaticRoute (i)
        self.GenLocalUser(i)
        self.GenStaticRoute(i)
        self.GenFWPolicy(i)


if __name__ == '__main__' :
    a = StressWAD()
    fgt_left    = DC (a.FGT_Left,  "fgt")
    #fgt_left.SetDebugLevel()

    #fgt_right.SetDebugLevel()
    fgt_left.DCTelnetDevice_FGT ()

    print "left ", fgt_left.Err
    #fgt_right.DCTelnetDevice_FGT ()
    #print "right", fgt_right.Err 
    for i in range (1 ,11) :
        a.GenAll(i)
        print "#" * 10, "Generate Config for FGT" , i
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


