#!/bin/sh

# Default valume is client<-->eth4====eth5<-->server
Client=eth4.100
Server=eth5.100
Delay=100
CMD=$1
Latency=150
Client_BW=1024kbit
Server_BW=1024kbit

if [ "$2" != "" ]
then 
	Client=$2
fi

if [ "$3" != "" ]
then 
	Server=$3
fi

if [ "$4" != "" ]
then
	Client_BW=$4
fi

if [ "$5" != "" ]
then 
	Server_BW=$5
fi

if [ "$6" != "" ]
then
	Delay=$6
	Latency=$((Delay/2))
fi

if [ "$CMD" == "stop" ]
then
	date
	echo "=========Stop TC========="
	tc qdisc del root dev $Client
	tc qdisc del root dev $Server
	echo "========= Done ==========" 
fi


if [ "$CMD" == "status" ]
then
	date
	echo "=========Client Side========"
	tc qdisc show dev $Client
	echo "=========Server Side========"
	tc qdisc show dev $Server
fi


if [ "$CMD" == "start" ]
then
	date
	tc qdisc add dev $Client root handle 1:0 netem delay "$Latency"ms
	tc qdisc add dev $Server root handle 2:0 netem delay "$Latency"ms
	tc qdisc add dev $Client parent 1:1 handle 10: tbf rate $Client_BW buffer 3000 latency "$Delay"ms
	tc qdisc add dev $Server parent 2:1 handle 20: tbf rate $Server_BW buffer 3000 latency "$Delay"ms 
fi
	echo "Start TC on ", $Client, $Server
if [ "$CMD" == "" ]
then 
echo "Usage:"
echo "${0} (start|stop|status) {Client_Interface} {Server_Interface} {Client_Bandwidth} {Server_Bandwidth}  {Delay}"
echo "Examples ${0} start eth4 eth5 64000 64000 150"
echo ""
fi

