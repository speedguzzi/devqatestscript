#!/usr/bin/python


import os, sys, time

class StressWAD ():
    def __init__ (self):
        self.FGT_Left = "10.10.0.16"
        self.FGT_Right = "10.10.0.15"
        self.FGT_Left_Username = "admin"
        self.FGT_Left_Password = ""
        self.FGT_Right_Username ="admin"
        self.FGT_Right_Password = ""
        self.Debug = 5
        self.FGT_Left_Cli = []
        self.FGT_Right_Cli =[]
        self.FGT_Left_ClientInterface  = "vlan705"
        self.FGT_Right_ClientInterface = "server_706"
        self.FGT_LeftTestInterface = "port8"
        self.FGT_RightTestInterface = "port8"
        
    def GenVdom (self,i=1):
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append ("config vdom")
        self.FGT_Left_Cli.append  ("edit test"+str(i))
        self.FGT_Right_Cli.append ("edit test"+str(i))
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Right_Cli.append ("end")
        return 0
    def GenVlan(self,i=1):
        self.FGT_Left_Cli.append ("config global")
        self.FGT_Left_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append ("edit test"+str(i)+"vlan"+str(i))
        self.FGT_Left_Cli.append ("set ip 50.0."+str(i)+".1/24")
        self.FGT_Left_Cli.append ("set allow http https ping snmp ssh  telnet")
        self.FGT_Left_Cli.append ("set vdom test"+str(i))
        self.FGT_Left_Cli.append ("set inter "+self.FGT_LeftTestInterface)
        self.FGT_Left_Cli.append ("set vlanid "+str(i))
        self.FGT_Left_Cli.append ("end")
        self.FGT_Left_Cli.append ("end")
        
        self.FGT_Right_Cli.append ("config global")
        self.FGT_Right_Cli.append ("config sys inter")
        self.FGT_Right_Cli.append ("edit test"+str(i)+"vlan"+str(i))
        self.FGT_Right_Cli.append ("set ip 50.0."+str(i)+".2/24")
        self.FGT_Right_Cli.append ("set allow http https ping snmp ssh telnet")
        self.FGT_Right_Cli.append ("set vdom test"+str(i))
        self.FGT_Right_Cli.append ("set inter "+self.FGT_RightTestInterface)
        self.FGT_Right_Cli.append ("set vlanid "+str(i))
        self.FGT_Right_Cli.append ("end")
        self.FGT_Right_Cli.append ("end")
        return 0

    def GenVdomLink(self,i=1):
        self.FGT_Left_Cli.append  ("config global")
        self.FGT_Right_Cli.append ("config global")
        self.FGT_Left_Cli.append  ("config system vdom-link")
        self.FGT_Right_Cli.append ("config system vdom-link")
        self.FGT_Left_Cli.append  ("edit h_t"+str(i)+"_")
        self.FGT_Right_Cli.append ("edit h_t"+str(i)+"_")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Right_Cli.append ("end")
        self.FGT_Left_Cli.append  ("config sys inter")
        self.FGT_Right_Cli.append ("config sys inter")
        self.FGT_Left_Cli.append  ("edit h_t"+str(i)+"_0")
        self.FGT_Right_Cli.append ("edit h_t"+str(i)+"_0")
        self.FGT_Left_Cli.append  ("set vdom home")
        self.FGT_Right_Cli.append ("set vdom home")
        self.FGT_Left_Cli.append  ("set ip 1.1."+str(i)+".1/24")
        self.FGT_Right_Cli.append ("set ip 2.2."+str(i)+".1/24")
        self.FGT_Left_Cli.append  ("set allow http https ping snmp ssh telnet")
        self.FGT_Right_Cli.append ("set allow http https ping snmp ssh telnet")
        self.FGT_Left_Cli.append  ("next")
        self.FGT_Right_Cli.append ("next")
        self.FGT_Left_Cli.append  ("edit h_t"+str(i)+"_1")
        self.FGT_Right_Cli.append ("edit h_t"+str(i)+"_1")
        self.FGT_Left_Cli.append  ("set vdom test"+str(i))
        self.FGT_Right_Cli.append ("set vdom test"+str(i))
        self.FGT_Left_Cli.append  ("set ip 1.1."+str(i)+".2/24")
        self.FGT_Right_Cli.append ("set ip 2.2."+str(i)+".2/24")
        self.FGT_Left_Cli.append  ("set allow http https ping snmp ssh telnet")
        self.FGT_Right_Cli.append ("set allow http https ping snmp ssh telnet")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Right_Cli.append ("end")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Right_Cli.append ("end")
        return 0

    def GenStaticRoute (self,i=1):
        # config static route in vdom home
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append ("config vdom")
        self.FGT_Left_Cli.append  ("edit home")
        self.FGT_Right_Cli.append ("edit home")
        self.FGT_Left_Cli.append  ("config router static")
        self.FGT_Right_Cli.append ("config router static")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append ("edit 0")
        self.FGT_Left_Cli.append  ("set dst 2.2."+str(i)+".0 255.255.255.0")
        self.FGT_Right_Cli.append ("set dst 1.1."+str(i)+".0 255.255.255.0")
        self.FGT_Left_Cli.append  ("set device h_t"+str(i)+"_0")
        self.FGT_Right_Cli.append ("set device h_t"+str(i)+"_0")
        self.FGT_Left_Cli.append  ("set gateway 1.1."+str(i)+".2")
        self.FGT_Right_Cli.append ("set gateway 2.2."+str(i)+".2")
        self.FGT_Left_Cli.append  ("end")     #Leave Static Route mode
        self.FGT_Right_Cli.append ("end")     #Leave Static Route mode
        self.FGT_Left_Cli.append  ("end")     #Leave vdom Home
        self.FGT_Right_Cli.append ("end")     #Leave vdom Home
        # config static route in vdom test
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append ("config vdom")
        self.FGT_Left_Cli.append  ("edit test"+str(i))
        self.FGT_Right_Cli.append ("edit test"+str(i))
        self.FGT_Left_Cli.append  ("config router static")
        self.FGT_Right_Cli.append ("config router static")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append ("edit 0")
        self.FGT_Left_Cli.append  ("set device h_t"+str(i)+"_1")
        self.FGT_Right_Cli.append ("set device h_t"+str(i)+"_1")
        self.FGT_Left_Cli.append  ("set gateway 50.0.0.2")
        self.FGT_Right_Cli.append ("set gateway 50.0.0.1")
        self.FGT_Left_Cli.append  ("end")         #leave the static routing configure 
        self.FGT_Right_Cli.append ("end")         #leave the static routing configure
        self.FGT_Left_Cli.append  ("end")     #Leave vdom test{i}
        self.FGT_Right_Cli.append ("end")     #Leave vdom test{i}
        return 0
    
    def GenVIP (self,i=1):
        #Config vip for test pc
        self.FGT_Right_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append  ("ed home")
        self.FGT_Left_Cli.append  ("ed home")
        self.FGT_Right_Cli.append  ("config fire vip")
        self.FGT_Left_Cli.append  ("config fire vip")
        self.FGT_Right_Cli.append  ("edit test"+str(i))
        self.FGT_Left_Cli.append  ("edit test"+str(i))
        self.FGT_Right_Cli.append  ("set extip 2.2."+str(i)+".10")
        self.FGT_Left_Cli.append  ("set extip 1.1."+str(i)+".10")
        self.FGT_Right_Cli.append  ("set extintf h_t"+str(i)+"_0")
        self.FGT_Left_Cli.append  ("set extintf h_t"+str(i)+"_0")
        self.FGT_Right_Cli.append  ("set mappedip 200.0.0.1")
        self.FGT_Left_Cli.append  ("set mappedip 100.0.0.1")
        self.FGT_Right_Cli.append  ("end")
        self.FGT_Left_Cli.append  ("end")
        #Use VIP setting in firewaself.FGT_Left_Cli.append  policy
        self.FGT_Right_Cli.append  ("config firewall policy")
        self.FGT_Left_Cli.append  ("config firewall policy")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ("set srcintf h_t"+str(i)+"_0")
        self.FGT_Left_Cli.append  ("set srcintf h_t"+str(i)+"_0")
        self.FGT_Right_Cli.append  ("set dstintf "+self.FGT_Right_ClientInterface)
        self.FGT_Left_Cli.append  ("set dstintf "+self.FGT_Left_ClientInterface)
        self.FGT_Right_Cli.append  ("set action accept")
        self.FGT_Left_Cli.append  ("set action accept")
        self.FGT_Right_Cli.append  ("set status enable ")
        self.FGT_Left_Cli.append  ("set status enable ")
        self.FGT_Right_Cli.append  ("set schedule always ")
        self.FGT_Left_Cli.append  ("set schedule always ")
        self.FGT_Right_Cli.append  ("set dstaddr test"+str(i))
        self.FGT_Left_Cli.append  ("set dstaddr test"+str(i))
        self.FGT_Right_Cli.append  ("set nat enable")
        self.FGT_Left_Cli.append  ("set nat enable")
        self.FGT_Right_Cli.append  ("set srcaddr all")
        self.FGT_Left_Cli.append  ("set srcaddr all") 
        self.FGT_Right_Cli.append  ('set service "ANY"')
        self.FGT_Left_Cli.append  ('set service "ANY"')
        self.FGT_Right_Cli.append  ("end")          #leave firewaself.FGT_Left_Cli.append  config context
        self.FGT_Left_Cli.append  ("end")          #leave firewaself.FGT_Left_Cli.append  config context
        self.FGT_Right_Cli.append  ("end")          #leave vdom home
        self.FGT_Left_Cli.append  ("end")          #leave vdom home
        return 0
    
    def GenFWPolicy (self,i=1):
        # This policy is for incoming traffic 
        self.FGT_Right_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append  ("edit test"+str(i))
        self.FGT_Left_Cli.append  ("edit test"+str(i))
        self.FGT_Right_Cli.append  ("config fire policy")
        self.FGT_Left_Cli.append  ("config fire policy")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ('set srcintf "test'+str(i)+'vlan'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set srcintf "test'+str(i)+'vlan'+str(i)+'"')
        self.FGT_Right_Cli.append  ('set dstintf "h_t'+str(i)+ '_1"' )
        self.FGT_Left_Cli.append  ('set dstintf "h_t'+str(i)+ '_1"' )
        self.FGT_Right_Cli.append  ('set srcaddr "all"')
        self.FGT_Left_Cli.append  ('set srcaddr "all"')
        self.FGT_Right_Cli.append  ('set dstaddr "all"')
        self.FGT_Left_Cli.append  ('set dstaddr "all"')
        self.FGT_Right_Cli.append  ("set action accept")
        self.FGT_Left_Cli.append  ("set action accept")
        self.FGT_Right_Cli.append  ('set schedule "always"')
        self.FGT_Left_Cli.append  ('set schedule "always"')
        self.FGT_Right_Cli.append  ('set service "ANY"')
        self.FGT_Left_Cli.append  ('set service "ANY"')
        self.FGT_Right_Cli.append  ('set logtraffic enable')
        self.FGT_Left_Cli.append  ('set logtraffic enable')
        self.FGT_Right_Cli.append  ("next")
        self.FGT_Left_Cli.append  ("next")
        # This policy for outgoing traffic
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ('set srcintf "h_t'+str(i)+ '_1"')
        self.FGT_Left_Cli.append  ('set srcintf "h_t'+str(i)+ '_1"')
        self.FGT_Right_Cli.append  ('set dstintf "test'+str(i)+'vlan'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set dstintf "test'+str(i)+'vlan'+str(i)+'"')
        self.FGT_Right_Cli.append  ('set srcaddr "all"')
        self.FGT_Left_Cli.append  ('set srcaddr "all"')
        self.FGT_Right_Cli.append  ('set dstaddr "all"')
        self.FGT_Left_Cli.append  ('set dstaddr "all"')
        self.FGT_Right_Cli.append  ("set action accept")
        self.FGT_Left_Cli.append  ("set action accept")
        self.FGT_Right_Cli.append  ('set schedule "always"')
        self.FGT_Left_Cli.append  ('set schedule "always"')
        self.FGT_Right_Cli.append  ('set service "ANY"')
        self.FGT_Left_Cli.append  ('set service "ANY"')
        self.FGT_Right_Cli.append  ('set logtraffic enable')
        self.FGT_Left_Cli.append  ('set logtraffic enable')
        self.FGT_Right_Cli.append  ("end")
        self.FGT_Left_Cli.append  ("end")
        self.FGT_Right_Cli.append  ("end")
        self.FGT_Left_Cli.append  ("end")
        return 0
    
    def GenWadCfg (self,i=1):
        self.FGT_Right_Cli.append  ("config vdom")
        self.FGT_Left_Cli.append  ("config vdom")
        self.FGT_Right_Cli.append  ("edit test"+str(i))
        self.FGT_Left_Cli.append  ("edit test"+str(i))
        self.FGT_Right_Cli.append  ("config wanopt peer")
        self.FGT_Left_Cli.append  ("config wanopt peer")
        self.FGT_Right_Cli.append  ('edit "left-test'+str(i)+'"')
        self.FGT_Left_Cli.append  ('edit "right-test'+str(i)+'"')
        self.FGT_Right_Cli.append  ("set ip 50.0."+str(i)+".1")
        self.FGT_Left_Cli.append  ("set ip 50.0."+str(i)+".2")
        self.FGT_Right_Cli.append  ("end")
        self.FGT_Left_Cli.append  ("end")
        # Below is WAD rule for http,tcp,smb
        self.FGT_Right_Cli.append  ("config wanopt rule")
        self.FGT_Left_Cli.append  ("config wanopt rule")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ("set port 80")
        self.FGT_Left_Cli.append  ("set port 80")
        self.FGT_Right_Cli.append  ("set proto http")
        self.FGT_Left_Cli.append  ("set proto http")
        self.FGT_Right_Cli.append  ('set peer "left-test'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set peer "right-test'+str(i)+'"')
        self.FGT_Right_Cli.append  ("next")
        self.FGT_Left_Cli.append  ("next")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ("set port 7000")
        self.FGT_Left_Cli.append  ("set port 7000")
        self.FGT_Right_Cli.append  ("set proto tcp")
        self.FGT_Left_Cli.append  ("set proto tcp")
        self.FGT_Right_Cli.append  ('set peer "left-test'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set peer "right-test'+str(i)+'"')
        self.FGT_Right_Cli.append  ("next")
        self.FGT_Left_Cli.append  ("next")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ("set port 139")
        self.FGT_Left_Cli.append  ("set port 139")
        self.FGT_Right_Cli.append  ("set proto cifs")
        self.FGT_Left_Cli.append  ("set proto cifs")
        self.FGT_Right_Cli.append  ('set peer "left-test'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set peer "right-test'+str(i)+'"')
        self.FGT_Right_Cli.append  ("next")
        self.FGT_Left_Cli.append  ("next")
        self.FGT_Right_Cli.append  ("edit 0")
        self.FGT_Left_Cli.append  ("edit 0")
        self.FGT_Right_Cli.append  ("set port 445")
        self.FGT_Left_Cli.append  ("set port 445")
        self.FGT_Right_Cli.append  ("set proto cifs")
        self.FGT_Left_Cli.append  ("set proto cifs")
        self.FGT_Right_Cli.append  ('set peer "left-test'+str(i)+'"')
        self.FGT_Left_Cli.append  ('set peer "right-test'+str(i)+'"')
        self.FGT_Right_Cli.append  ("end")
        self.FGT_Left_Cli.append  ("end")
        return 0
    



v=199
a=StressWAD()
a.GenVdom(v)
a.GenVlan(v)
a.GenVdomLink(v)
a.GenStaticRoute (v)
a.GenVIP(v)
a.GenFWPolicy(v)
a.GenWadCfg(v)

print '=' * 40
for i in range(len(a.FGT_Left_Cli)) :
    print a.FGT_Left_Cli[int(i)]
print '=' * 40
for i in range (len(a.FGT_Right_Cli)) :
    print a.FGT_Right_Cli[int(i)]

