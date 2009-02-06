#
# This script will generate FOS 4.0 Wanopt relate CLI 
#

import os, sys

CFG='./tbl-wad.cfg'
Platform = 'FG50BH'
DEV = {'wad-policy': '32', 'wad-auth-group': '16', 'wad-peer': '32', 'wad-ssl-server': '32'}

TMP="/tmp"

def LoadCFG (C=CFG):
    return 1

def PrintDEV ():
    print type (DEV), len(DEV)

def tbl_wad_004 ():
    wad_peer_name_prefix = 'ABDEFGHIJKLMNOPQRSTUVWXYZabcdef'
    #
    # This function will generate Wanopt peer to {tmp}/tbl-wad-001.cfg
    #
    filename = TMP + '/' + sys._getframe().f_code.co_name + '.cfg'
    f = open (filename, 'w')
    f.write ('config wanopt peer \n')
    for i in range (int (DEV.get('wad-peer'))) :
        f.write ('edit '+wad_peer_name_prefix +str (i)+'\n')
        f.write ('  set ip 2.2.2.' + str (i+1)+'\n')
        f.write ('next'+'\n')
    f.write ('end')
    f.close()
    
def tbl_wad_001 ():
    wad_auth_group_prefix = 'authgroup_ABCDEFGHIJKLMNOPQRSTUV'
    #
    # This function will generate Wanopt auth-peer to /tmp
    #
    filename = TMP + '/' + sys._getframe().f_code.co_name + '.cfg'
    f = open (filename, 'w')
    f.write ('config wanopt auth \n')
    for i in range (int (DEV.get('wad-auth-group'))) :
        f.write ('edit ' + wad_auth_group_prefix + str (i) + '\n')
        f.write (' set auth psk \n')
        f.write (' set psk ' + wad_auth_group_prefix +'\n')
        f.write ('next \n')
    f.write ('end \n')
    f.close()
    
def tbl_wad_007 ():
    #
    # this function will generate Wanopt rule to /tmp
    #
    filename =   TMP + '/' +sys._getframe().f_code.co_name + '.cfg'
    f = open (filename, 'w')
    f.write ('config wan rule \n')
    for i in range (int(DEV.get('wad-policy'))) :
        f.write ('edit 0 \n')
        f.write ('set port ' + str (1000+i) + '\n')
        f.write ('set method byte \n')
        f.write ('set peer ABDEFGHIJKLMNOPQRSTUVWXYZabcdef0 \n')
        f.write ('next \n')
    f.write ('end\n')
    f.close()
    
def tbl_wad_010 ():
    #
    # This function will generate Wanopt ssl-server to /tmp
    #
    wad_ssl_server_prefix = 'ssl-server_ABCDEFGHIJKLMNOPQRST'
    filename = TMP + '/' +sys._getframe().f_code.co_name + '.cfg'
    f = open (filename, 'w')
    f.write ('config wanopt ssl \n')
    for i in range (int(DEV.get('wad-ssl-server'))) :
        f.write (' edit ' + wad_ssl_server_prefix +str (i+1)+ '\n')
        f.write ('  set ip 1.1.1.' + str (i+1) + '\n')
        f.write ('  set ssl-cert Fortinet_Firmware \n')
        f.write ('  set port 443 \n')
        f.write (' next \n')
    f.write ('end \n')
    f.close ()
tbl_wad_001()
tbl_wad_004()
tbl_wad_010()    
tbl_wad_007()