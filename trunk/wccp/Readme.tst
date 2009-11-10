###################################
# What's in this file
#   * folder description
#   * 


###################################

A. Folder Description

--+---script	# Test Script folder
  |     |
  |     +---topo-xxxx	# script to set topology
  |    
  +---TestCase  # to store all test case , use test id to create sub-folder
  |
  +---log	# to store test log . Console output, packate capture.

B. Tools 
	B1. 	Topology Setup
		
	B2. 	Verify tools

Appendix A:
	Depend tools on PC
		* vconfig 		# to configure vlan interface on pc
		* tunctl 		# to create loopback interface on pc
		* socat			# netcat++ to simulator TCP/UDP Server/Client
		* nc			# arbitrary TCP and UDP connections and listens

