#
import time,re,sys,platform,socket,telnetlib

#if (platform.system() == "Linux") :
#	ROOT="/root/workspace/wx/"
#	CFG="cfg/device.cfg"
#elif (platform.system() == "Microsoft") :
#	CFG='cfg\\device.cfg'
#	ROOT='C:\\Users\\henry\\workspace\\wx\\'


"""
Err :
    1   -> IP or telnet port not reachable
    2   -> EOF, Server close telnet session
    3   -> reserved
    4   -> reserved
    100 -> Configure File Error
    101 -> Reserved
"""

""" 
	The devicecontrol.py depend cfg/device.cfg
	format should be 
	[device s/n]
	ipaddress=1.1.1.1/24
	type={fgt|cisco_router|cisco_cat|linux}
	platform={descript}
	console={telnet://10.10.0.2:2001|telnet://10.10.0.123,minicom com3}
"""
class DC ():
    def __init__ (self,IP, type):
        self.DEBUG = 0
        self.DeviceType = type
        self.DeviceMgmtPort = "23"
        self.Platform = ""
        self.DeviceIP = IP          # Ex: DeviceIP=10.10.0.23:23
        self.DevicePowerControl = "" # Now only support DLT uu.pl 4.1 version
        self.Err = 0
        self.DeviceAccessMode = ""  # support Telnet, TS : Terminal Server
        self.DeviceUsername = "admin"
        self.DevicePassword = ""
        self.DeviceName = ""        # Hostname Linux,Windows, FGT, Router
        self.DeviceSerialNumber = "" # FGT, Serial number, 
        self.Device_T =""
        if (platform.uname()[0] != "Linux") :
            self.DebPrint ("The platform is "+platform.uname()[0]+" not fully test on it",0)
            
    def DebPrint (self, MSG,DebugLevel=5):
        if (DebugLevel > self.DEBUG) or (self.DEBUG == -1):
            print time.ctime(),":",str (sys._getframe(1).f_code.co_name)+":"+str (sys._getframe(1).f_lineno),"  ",MSG
    def SetDebugLevel (self, Level=-1 ):
        #-1 is mean turn all debug 
        self.DEBUG = Level
        return 0
    def SetDevicePoserControl (self, CLI) :
        self.DevicePowerControl = CLI
        return 0
    
    def SetDeviceUsername (self, Username, Password):
        self.DevicePassword = Password
        self.DeviceUsername = Username
        return 0
    
    def SetDeviceIP (self, IP):
        self.DeviceIP = IP
        return 0
    
    def DCTelnetDevice_FGT(self) :
        self.DebPrint( "Connect to FGT "+self.DeviceIP)
        try :
            self.Device_T=telnetlib.Telnet(self.DeviceIP,self.DeviceMgmtPort)
            print self.DeviceIP,self.DeviceMgmtPort
            L=self.Device_T.read_until("login: ",15)
            print "a: ",L
            self.Device_T.write (self.DeviceUsername + "\n")
            print self.DeviceUsername
            L=self.Device_T.read_until("assword: ",15)
            print "b: ",L
            self.Device_T.write(self.DevicePassword + "\r\n")
            self.DebPrint (L,1)
        except socket.error :
            self.Err=2 # error
            self.DebPrint( "check IP and telnet service\n",1)
            return self.Err
        except EOFError :
            self.Err=1 # close by peer
            self.DebPrint( "Server close telnet port\n",1)
            return self.Err
        return self.Err
 
    
    def DCTelnetTSClearLine(self, ts,port) :
        self.DebPrint(":clear line "+ts+" port: "+port)
        try :
            ts=telnetlib.Telnet(ts)
        except socket.error :
            print "Error, can't connect to TS , STOP running"
            print " The TS (2511/2509) must be config as"
            print "    no login password"
            print "    enable password qa1234"
            print "    privi exec level 1 clear line"
            return 1
        ts.read_until ("#",10)
        line = "clear line " + str (int(port)-2000)+"\n"
        self.DebPrint (line)
        ts.write (line)
        ts.read_until ("[confirm]",10)
        ts.write ("\n")
        ts.close()
        return 0 #OK

    def DCTelnetDevice_Router(self,IP):
        self.DebPrint (IP,1)
        try :
            T=telnetlib.Telnet(IP)
            L=T.read_until('#',15)
            self.DebPrint ( L,3)
        except socket.error,socket.connect:
            self.Err=2
            self.DebPrint ( "IP or Port can't reach",1)
            return 1
        except EOFError :
            self.Err=1
            self.DebPrint ( "Router Close Telnet",1)
            return 2
        self.Err=0
        return T

    def DCTelnetDeviceConsole_Router (self,Console) :
        temp = Console.split(':')
        temp[1]=temp[1].strip("//")
        DebPrint ( temp)
        if (temp[0] != "telnet" ) :return 1 # Not support protocol
        while (1) :                         # Try to connect , if fail, call clear TS line
            try :
                if (len(temp) ==3) :
                    T=telnetlib.Telnet(temp[1],temp[2])
                elif (len(temp) ==2) :
                    T=telnetlib.Telnet(temp[1])
                else :
                    self.DebPrint ( "Config file may error"+Console,2)
                    self.Err=100 # can't run ,
                    return 
            except socket.error :
                self.DebPrint ( "Call Clear TS Line",1)
                self.DCTelnetTSClearLine (temp[1],temp[2])
                self.DebPrint ( "Clear TS Line Done, try again",1)
                continue
            break
        T.write("\n")
        T.write("\n")
        while (1) :                         # Try to reach FGT Login: , If Not, then send exit and end, then try again
            line=T.read_until(">",5)
            m=re.search('>$',line)
            if m :
                self.DebPrint("Match Login Phase:"+line, 2)
                T.write("en\n")
 # Not support en with password           T.read_until("Password: ",10)
 #           T.write("\n")
                break
            else :
                self.DebPrint ("not match login phase, will send end:"+line, 2)
                T.write("exit\n")
                T.write("end\n")
        self.Err=0
        return T

    def DCTelnetDevice_Windows(self,IP):
        self.DebPrint ( "Connect to Windows "+IP)
        try :
            T=telnetlib.Telnet(IP)
            L=T.read_until("login: ",15)
            self.DebPrint (L,5)
    #        T.write ('lab  \r')
            T.write ('administrator\r')
            L=T.read_until("assword:",15)
            self.DebPrint (L,5)
            T.write('qa1234\r')
            L=T.read_until(">",10)
            self.DebPrint (L,5)
        except socket.error :
            print "Please check Guest IP and Telnet Service running status\n"
            self.Err=2
            return  # can't resolve.
        except EOFError :
            print "Please check Guest OS, May not allow more telnet session \n"
            T.close()
            self.Err=1
            return
        self.Err=0
        return T


    def DCTelnetDeviceConsole_FGT(self, Console) :
        temp = Console.split(':')
        temp[1]=temp[1].strip("//")
        self.DebPrint (temp,1)
        if (temp[0] != "telnet" ) :return 1 # Not support protocol
        while (1) :                         # Try to connect , if fail, call clear TS line
            try :
                if (len(temp) == 3) :
                    T=telnetlib.Telnet(temp[1],temp[2])
                elif (len(temp) == 2) :
                    T=telnetlib.Telnet(temp[1])
                else:
                    self.Err=100 #Error Configure file
                    self.DebPrint ( Console,1)
                    return
                break
            except socket.error,socket.connect :
                self.DCDeviceTSClearLine ("10.10.0.2","2001")
                self.DebPrint ( "call clear line done",3)
                continue
        T.write("\n")
        T.write("\r")
        while (1) :                         # Try to reach FGT Login: , If Not, then send exit and end, then try again
            line=T.read_until("login: ",5)
            m=re.search('login: $',line)
            if m :
                self.DebPrint( "Match Login Phase:"+line,3)
                T.write("admin\n")
                T.read_until("Password: ",10)
                T.write("\n")
                break
            else :
                self.DebPrint( "not match login phase, will send end:"+line,3)
                T.write("exit\n")
                T.write("end\n")
        return T
    def DCUploadCFG_FGT(self,CLI,Prompt="#"):
        self.Err=0
        self.DebPrint ( self.Device_T.host+" "+CLI[0])
        if not self.Device_T.sock_avail() :
            self.DebPrint ("It's not a live Telnet Session, May timeouted.")
            self.DCTelnetDevice_FGT()
        try :
            for C in CLI[:] :
                self.Device_T.write (C+"\n")
                #self.DebPrint (C ,1)
                L = self.Device_T.read_until (Prompt,15)
                self.DebPrint (L ,1),
        except socket.error, socket.connect :
            self.Err=1
            self.DebPrint ("Connect Error")
        except EOFError :
            self.Err=2
            self.DebPrint ("Server close Telnet Session")
        return self.Err     
#    def DCInitDevice_FGT(self,Dev,mode="nat") :
        """ Connect to device Console,
        Find/Load Init Config then apply to Device. 
        Now support FGT only
        """
        #type = Config.get(Dev,"type")
        #if (type == "FGT") :
        #    TS = DCTelnetDeviceConsole_FGT (Config.get(Dev,"console"))
        #else :
        #    return 1 #not support device
        # find Init configure file
        #if (mode == "nat") :
        #    C = ROOT+"cfg/fgt_init/"+Dev[:6]+"/nat_init.cfg"
        #elif (mode == "tp") :
         #   C = ROOT+"cfg/fgt_init/"+Dev[:6]+"/tp_init.cfg"
        #self.rint ( C,3)
        #F=open (C,"rb")
        #for line in F:
            #print line
           # TS.write (line+"\n")
          #  l=TS.read_until("#",10)
         #   print l
        #TS.close()
        #self.DebPrint ( "init FGT down",3)
    def DCSetWANSpeed_Router (self, IP,Interface, ClockRate) :
        self.DebPrint (IP + ' '+Interface+' '+ ClockRate )
        T = DCTelnetDevice_Router (IP)
        T.write ("config t")
        L=T.read_until ("#",15)
        self.DebPrint (L, 4)
        T.write ("inter "+Interface)
        L=T.read_until ("#",15)
        self.DebPrint (L, 4)
        T.write ("clock rate "+ClockRate)
        L=T.read_until ("#",15)
        self.DebPrint (L, 4)
        T.write ("end")
        L=T.read_until ("#",15)
        self.DebPrint (L, 4)
        T.write ("wr")
        L=T.read_until ("#",15)
        self.DebPrint (L, 4)
        T.close()
    def DCSetWANSpeed_TC (self,Eth_Client,Eth_Server, Client_Speed,Server_Speed,Delay) :
        CLI=ROOT+'/wan/wanemu.sh '+Eth_Client+ \
            " "+Eth_Server + \
            " "+Client_Speed + \
            " "+Server_Speed + \
            " "+Delay
        Lines = os.popen (CLI)
        tmp=Lines.read()
        self.DebPrint (tmp,4)
        Lines.close()
    

    def DCUploadCFG_Router(self,T,CLI,Prompt="#"):
        """
    DCUploadCFG_Router(T,CLI,Prompt)
    T := telnetlib.Telnet session to FGT
    CLI := CLI will apply to Cisco router or Catalyst , LIST
    Prompt := default use "#", will .read_until(Prompt,15) for each CLI
    """
        self.Err=0
        self.DebPrint ( T.host+" "+CLI[0])
        if not T.sock_avail() :
            self.DebPrint ("It's not a live Telnet Session")
        try :
            for C in CLI[:] :
                T.write (C+"\n")
                L=T.read_until (Prompt,15)
                self.DebPrint (L)
        except socket.error, socket.connect :
            self.Err=1
            self.DebPrint ("Connect Error")
        except EOFError :
            self.Err=2
            self.DebPrint ("Server close Telnet Session")
        return self.Err


if __name__ == '__main__' :
    #Config=ConfigParser.ConfigParser()
    #Config.read(ROOT+CFG)
    #S = Config.sections()
    #if (DEBUG >3) : print (S)  # debug 
    #O = Config.options (S[0])
    TW1=DC.DCTelnetDevice_FGT ("10.10.0.33")
    #DCInitDevice_FGT(S[5])
    print DC.Err
    CLI =["get sys inter","get hard status","exec date",""]
    if not Err :
        DC.DCUploadCFG_FGT(TW1,CLI)
