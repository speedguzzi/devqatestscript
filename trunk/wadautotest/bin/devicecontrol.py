#
import time,re,sys,platform,socket,telnetlib

#if (platform.system() == "Linux") :
#	ROOT="/root/workspace/wx/"
#	CFG="cfg/device.cfg"
#elif (platform.system() == "Microsoft") :
#	CFG='cfg\\device.cfg'
#	ROOT='C:\\Users\\henry\\workspace\\wx\\'

ERR=0
"""
ERR :
    1   -> IP or telnet port not reachable
    2   -> EOF, Server close telnet session
    3   -> reserved
    4   -> reserved
    100 -> Configure File Error
    101 -> Reserved
"""
DEBUG=5
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
    def __init__ ():
        self.DEBUG = 0
        self.Platform = ""
        self.DeviceIP = ""          # Ex: DeviceIP=10.10.0.23:23
        self.DevicePowerControl = "" # Now only support DLT uu.pl 4.1 version
        self.Err = 0
        self.DeviceAccessMode = ""  # support Telnet, TS : Terminal Server
        self.DeviceUsername = ""
        self.DevicePassword = ""
        self.DeviceName = ""        # Hostname Linux,Windows, FGT, Router
        self.DeviceSerialNumber = "" # FGT, Serial number, 
    def DebPrint (MSG,DebugLevel=5):
        if (DebugLevel > self.DEBUG) or (DEBUG == -1):
            print time.ctime(),":",sys._getframe(1).f_code.co_name,": ",MSG
    def SetDebugLevel (Level=-1 ):
        #-1 is mean turn all debug 
        self.DEBUG == Level
        return 0
    def SetDevicePoserControl (CLI) :
        self.DevicePowerControl = CLI
        return 0
    
    def SetDeviceUsername (Username, Password):
        self.DevicePassword = Password
        self.DeviceUsername = Username
        return 0
    
    def SetDeviceIP (IP):
        self.DeviceIP = IP
        return 0
    
    def DCTelnetDevice_FGT(IP,Port=23) :
        DebPrint( "Connect to FGT "+IP)
        try :
            T=telnetlib.Telnet(IP,Port)
            L=T.read_until("login: ",15)
            T.write (self.DeviceUsername + "\n")
            L=T.read_until("assword: ",15)
            T.write(self.DevicePassword + "\r\n")
            DebPrint (L)
        except socket.error :
            Err=2 # error
            DebPrint( "check IP and telnet service\n",1)
            return err
        except EOFerror :
            Err=1 # close by peer
            DebPrint( "Server close telnet port\n",1)
            return Err
        return T
 
    
def DCTelnetTSClearLine(ts,port) :
    global ERR
    DBPrint(":clear line "+ts+" port: "+port)
    try :
        ts=telnetlib.Telnet(ts)
    except socket.error :
        print "Error, can't connect to TS , STOP running"
        print " The TS (2511/2509) must be config as"
        print "    no login password"
        print "    enable password qa1234"
        print "    privi exec level 1 clear line"
        exit (1)
    ts.read_until ("#",10)
    line = "clear line " + str (int(port)-2000)+"\n"
    if (DEBUG > 3) : print sys._getframe(0).f_code.co_name+line
    ts.write (line)
    ts.read_until ("[confirm]",10)
    ts.write ("\n")
    ts.close()
    return 0 #OK

def DCTelnetDevice_Router(IP):
    global ERR
    DBPrint ( IP)
    try :
        T=telnetlib.Telnet(IP)
        L=T.read_until('#',15)
        DBPrint ( L,3)
    except socket.error,socket.connect:
        ERR=2
        DBPrint ( "IP or Port can't reach",1)
        return
    except EOFError :
        ERR=1
        DBPrint ( "Router Close Telnet",1)
        return
    ERR=0
    return T

def DCTelnetDeviceConsole_Router (Console) :
    global ERR
    temp = Console.split(':')
    temp[1]=temp[1].strip("//")
    DBPrint ( temp)
    if (temp[0] != "telnet" ) :return 1 # Not support protocol
    while (1) :                         # Try to connect , if fail, call clear TS line
        try :
            if (len(temp) ==3) :
                T=telnetlib.Telnet(temp[1],temp[2])
            elif (len(temp) ==2) :
                T=telnetlib.Telnet(temp[1])
            else :
                DBPrint ( "Config file may error"+Console,2)
                ERR=100 # can't run ,
                return
            break
        except socket.error :
            DBPrint ( "Call Clear TS Line",1)
            DCDeviceTSClearLine (temp[1],temp[2])
            DBPrint ( "Clear TS Line Done, try again",1)
            continue
    T.write("\n")
    T.write("\n")
    while (1) :                         # Try to reach FGT Login: , If Not, then send exit and end, then try again
        line=T.read_until(">",5)
        m=re.search('>$',line)
        if m :
            if (DEBUG > 2) : print "Match Login Phase:"+line
            T.write("en\n")
 # Not support en with password           T.read_until("Password: ",10)
 #           T.write("\n")
            break
        else :
            if (DEBUG >2) : print "not match login phase, will send end:"+line
            T.write("exit\n")
            T.write("end\n")
    ERR=0
    return T

def DCTelnetDevice_Windows(IP):
    global ERR
    DBPrint ( "Connect to Windows "+IP)
    try :
        T=telnetlib.Telnet(IP)
        L=T.read_until("login: ",15)
        DBPrint (L,5)
#        T.write ('lab  \r')
        T.write ('administrator\r')
        L=T.read_until("assword:",15)
        DBPrint (L,5)
        T.write('qa1234\r')
        L=T.read_until(">",10)
        DBPrint (L,5)
    except socket.error :
        print "Please check Guest IP and Telnet Service running status\n"
        ERR=2
        return  # can't resolve.
    except EOFError :
        print "Please check Guest OS, May not allow more telnet session \n"
        T.close()
        ERR=1
        return
    ERR=0
    return T


def DCTelnetDeviceConsole_FGT(Console) :
    global ERR
    temp = Console.split(':')
    temp[1]=temp[1].strip("//")
    DBPrint ( temp)
    if (temp[0] != "telnet" ) :return 1 # Not support protocol
    while (1) :                         # Try to connect , if fail, call clear TS line
        try :
            if (len(temp) == 3) :
                T=telnetlib.Telnet(temp[1],temp[2])
            elif (len(temp) == 2) :
                T=telnetlib.Telnet(temp[1])
            else:
                ERR=100 #Error Configure file
                DBPrint ( Console,1)
                return
            break
        except socket.error,socket.connect :
            DCDeviceTSClearLine ("10.10.0.2","2001")
            DBPrint ( "call clear line done",3)
            continue
    
    T.write("\n")
    T.write("\r")
    while (1) :                         # Try to reach FGT Login: , If Not, then send exit and end, then try again
        line=T.read_until("login: ",5)
        m=re.search('login: $',line)
        if m :
            DBPrint( "Match Login Phase:"+line,3)
            T.write("admin\n")
            T.read_until("Password: ",10)
            T.write("\n")
            break
        else :
            DBPrint( "not match login phase, will send end:"+line,3)
            T.write("exit\n")
            T.write("end\n")
    return T

        
def DCInitDevice_FGT(Dev,mode="nat") :
    """ Connect to device Console,
    Find/Load Init Config then apply to Device. 
    Now support FGT only
    """
    global ERR
    type = Config.get(Dev,"type")
    if (type == "FGT") :
        TS = DCTelnetDeviceConsole_FGT (Config.get(Dev,"console"))
    else :
        return 1 #not support device
    # find Init configure file
    if (mode == "nat") :
        C = ROOT+"cfg/fgt_init/"+Dev[:6]+"/nat_init.cfg"
    elif (mode == "tp") :
        C = ROOT+"cfg/fgt_init/"+Dev[:6]+"/tp_init.cfg"
        
    DBprint ( C,3)
    F=open (C,"rb")
    for line in F:
        print line
        TS.write (line+"\n")
        l=TS.read_until("#",10)
        print l
    TS.close()
    DBPrint ( "init FGT down",3)
def DCSetWANSpeed_Router (IP,Interface, ClockRate) :
    DBPrint (IP + ' '+Interface+' '+ ClockRate )
    T = DCTelnetDevice_Router (IP)
    T.write ("config t")
    L=T.read_until ("#",15)
    DBPrint (L, 4)
    T.write ("inter "+Interface)
    L=T.read_until ("#",15)
    DBPrint (L, 4)
    T.write ("clock rate "+ClockRate)
    L=T.read_until ("#",15)
    DBPrint (L, 4)
    T.write ("end")
    L=T.read_until ("#",15)
    DBPrint (L, 4)
    T.write ("wr")
    L=T.read_until ("#",15)
    DBPrint (L, 4)
    T.close()
def DCSetWANSpeed_TC (Eth_Client,Eth_Server, Client_Speed,Server_Speed,Delay) :
    CLI=ROOT+'/wan/wanemu.sh '+Eth_Client+ \
         " "+Eth_Server + \
         " "+Client_Speed + \
         " "+Server_Speed + \
         " "+Delay
    Lines = os.popen (CLI)
    tmp=Lines.read()
    DBPrint (tmp,4)
    Lines.close()
    
def DCUploadCFG_FGT(T,CLI,Prompt="#"):
    """
DCUploadCFG_FGT(T,CLI,Prompt)
T := telnetlib.Telnet session to FGT
CLI := CLI will apply to FGT , LIST
Prompt := default use "#", will .read_until(Prompt,15) for each CLI
    """
    global ERR
    ERR=0
    DBPrint ( T.host+" "+CLI[0])
    if not T.sock_avail() :
        DBPrint ("It's not a live Telnet Session")
    try :
        for C in CLI[:] :
            T.write (C+"\n")
            L=T.read_until (Prompt,15)
            DBPrint (L)
    except socket.error, socket.connect :
        ERR=1
        DBPrint ("Connect Error")
    except EOFError :
        ERR=2
        DBPrint ("Server close Telnet Session")
    return ERR 
def DCUploadCFG_Router(T,CLI,Prompt="#"):
    """
DCUploadCFG_Router(T,CLI,Prompt)
T := telnetlib.Telnet session to FGT
CLI := CLI will apply to Cisco router or Catalyst , LIST
Prompt := default use "#", will .read_until(Prompt,15) for each CLI
    """
    global ERR
    ERR=0
    DBPrint ( T.host+" "+CLI[0])
    if not T.sock_avail() :
        DBPrint ("It's not a live Telnet Session")
    try :
        for C in CLI[:] :
            T.write (C+"\n")
            L=T.read_until (Prompt,15)
            DBPrint (L)
    except socket.error, socket.connect :
        ERR=1
        DBPrint ("Connect Error")
    except EOFError :
        ERR=2
        DBPrint ("Server close Telnet Session")
    return ERR

if __name__ == '__main__' :
    #Config=ConfigParser.ConfigParser()
    #Config.read(ROOT+CFG)
    #S = Config.sections()
    #if (DEBUG >3) : print (S)  # debug 
    #O = Config.options (S[0])
    TW1=DCTelnetDevice_FGT ("10.10.0.33")
    #DCInitDevice_FGT(S[5])
    print ERR
    CLI =["get sys inter","get hard status","exec date",""]
    if not ERR :
        DCUploadCFG_FGT(TW1,CLI)
