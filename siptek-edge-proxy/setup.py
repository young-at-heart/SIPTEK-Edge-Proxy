#!/usr/bin/python3

### import modules
import os
import socket
import netifaces as ni
from requests import get
from colorama import Fore

### find nic and get public ip address
nic_list = socket.if_nameindex()
m = 1 ### interface index
n = m+1 ### interface index
advertise_ip = get('https://api.ipify.org').text

### define functions
def menu():
    print(Fore.GREEN+"[1] Option 1 show nic id and ip address.")
    print("[2] Option 2 set ip address. PLEASE RUN THIS OPTION IN CONSOLE OR YOU WILL BE DISCONNECTED.")
    print("[3] Option 3 set IP-PBX destination.")
    print("[4] Option 4 monitor system performance.")
    print("[0] Option 0 exit the program.")

def disp_menu():
    print(Fore.GREEN+"[1] Choice 1 show IP-PBX ip address.")
    print("[2] Choice 2 add IP-PBX.")
    print("[3] Choice 3 delete IP-PBX.")
    print("[0] Choice 0 exit the program.")

def netinfo():
    host_name = socket.gethostname()
    print(Fore.CYAN+f"Hostname: {host_name}")
    nic_list = socket.if_nameindex()
    for i in range(m,n+1):
      print(Fore.CYAN+f"Interface: {nic_list[i][1]}")
      cmd = "ip a | grep inet | grep "+nic_list[i][1]
      os.system(cmd)
    print(Fore.CYAN+"Public ip address: by ipify.org")
    print(Fore.CYAN+f"    {advertise_ip}")

def sysconfig(extern_nic, extern_ip, extern_mask, net_gw, intern_nic, intern_ip, intern_mask):
    if advertise_ip == "":
      print(Fore.RED+"cannot get public ip, please check internat connection.")
    else:
      ### set nic
      os.system('echo "### The loopback network interface" > /etc/network/interfaces')
      os.system('echo "auto lo" >> /etc/network/interfaces')
      os.system('echo "iface lo inet loopback" >> /etc/network/interfaces')
      os.system('echo "### The external network interface" >> /etc/network/interfaces')
      os.system('echo "allow-hotplug "'+extern_nic+' >> /etc/network/interfaces')
      os.system('echo "iface "'+extern_nic+' inet static >> /etc/network/interfaces')
      os.system('echo "address "'+extern_ip+' >> /etc/network/interfaces')
      os.system('echo "netmask "'+extern_mask+' >> /etc/network/interfaces')
      os.system('echo "gateway "'+net_gw+' >> /etc/network/interfaces')
      os.system('echo "dns-nameservers 8.8.8.8 8.8.4.4" >> /etc/network/interfaces')
      os.system('echo "### The internal network interface" >> /etc/network/interfaces')
      os.system('echo "allow-hotplug "'+intern_nic+' >> /etc/network/interfaces')
      os.system('echo "iface "'+intern_nic+' inet static >> /etc/network/interfaces')
      os.system('echo "address "'+intern_ip+' >> /etc/network/interfaces')
      os.system('echo "netmask "'+intern_mask+' >> /etc/network/interfaces')
      ### set firewalld
      cmd = "sed -i 's/<interface.*/<interface name=\""+extern_nic+"\"\/>/' /etc/firewalld/zones/public.xml"
      os.system(cmd)
      ### set rtpengine
      cmd = "sed -i 's/interface.*/interface = int\/"+intern_ip+";ext\/"+extern_ip+"!"+advertise_ip+"/' /etc/rtpengine/rtpengine.conf"
      os.system(cmd)
      ### set kamailio
      cmd = "sed -i 's/#!define SIPADDRINTERN.*/#!define SIPADDRINTERN \"sip:"+intern_ip+":5060\"/' /etc/kamailio/kamailio-local.cfg"
      os.system(cmd)
      cmd = "sed -i 's/listen=udp.*.extern.*/listen=udp:"+extern_ip+":5060 advertise "+advertise_ip+":5060 name \"extern\"/' /etc/kamailio/kamailio-local.cfg"
      os.system(cmd)
      cmd = "sed -i 's/listen=udp.*.intern.*/listen=udp:"+intern_ip+":5060 name \"intern\"/' /etc/kamailio/kamailio-local.cfg"
      os.system(cmd)

      ### restart network and firewalld
      os.system('/usr/sbin/ifdown '+nic_list[m][1])
      os.system('/usr/sbin/ifup '+nic_list[m][1])
      os.system('/usr/sbin/ifdown '+nic_list[n][1])
      os.system('/usr/sbin/ifup '+nic_list[n][1])
      os.system('systemctl restart firewalld')

      ### restart rtpengine and kamailio
      os.system('systemctl restart rtpengine')
      os.system('systemctl restart kamailio')
      print("restart services completed.")

### start first page

os.system('clear')
print(Fore.GREEN+"Siptek edge proxy setting menu.")
print()
menu()
print()
option = int(input("Enter your option: "))

while option !=0:
  ### option 1
  if option == 1:
    os.system('clear')
    print("Siptek edge proxy setting menu.")
    print()
    print("Option 1 show nic id and ip address.")
    print()
    netinfo()
  ### option 2
  elif  option == 2:
    os.system('clear')
    print("Siptek edge proxy setting menu.")
    print()
    print("Option 2 set ip address. PLEASE RUN THIS OPTION IN CONSOLE OR YOU WILL BE DISCONNECTED.")
    print()
    extern_nic = input("Please select external nic ("+nic_list[m][1]+", "+nic_list[n][1]+") ")
    while extern_nic not in (nic_list[m][1], nic_list[n][1]):
      print(Fore.RED+"external nic is not correct, please try again.")
      extern_nic = input(Fore.GREEN+"Please select external nic ("+nic_list[m][1]+", "+nic_list[n][1]+") ")
    print(Fore.CYAN+f"external nic = {extern_nic}")
    extern_ip = input(Fore.GREEN+"Please enter external ip address (ex. 192.168.1.5) ")
    while extern_ip == "":
      print(Fore.RED+"external ip is emplty, please try again.")
      extern_ip = input(Fore.GREEN+"Please enter external ip address (ex. 192.168.1.5) ")
    print(Fore.CYAN+f"external ip address = {extern_ip}")
    extern_mask = input(Fore.GREEN+"Please enter external subnet mask (ex. 255.255.255.0) ")
    while extern_mask == "":
      print(Fore.RED+"external subnet mask is empty, please try again.")
      extern_mask = input(Fore.GREEN+"Please enter external subnet mask (ex. 255.255.255.0) ")
    print(Fore.CYAN+f"external subnet mask = {extern_mask}")
    net_gw = input(Fore.GREEN+"Please enter network gateway (ex. 192.168.1.1) ")
    while net_gw == "":
      print(Fore.RED+"network gateway is empty, please try again.")
      net_gw = input(Fore.GREEN+"Please enter network gateway (ex. 192.168.1.1) ")
    print(Fore.CYAN+f"network gateway = {net_gw}")
    if extern_nic == nic_list[m][1]:
       intern_nic = nic_list[n][1]
    else:
       intern_nic = nic_list[m][1]
    print(Fore.GREEN+f"internal nic = {intern_nic}")
    intern_ip = input(Fore.GREEN+"Please enter internal ip address (ex. 172.16.10.10) ")
    while intern_ip == "":
      print(Fore.RED+"internal ip is empty, please try again.")
      intern_ip = input(Fore.GREEN+"Please enter internal ip address (ex. 172.16.10.10) ")
    print(Fore.CYAN+f"internal ip address = {intern_ip}")
    intern_mask = input(Fore.GREEN+"Please enter internal subnet mask (ex. 255.255.255.0) ")
    while intern_mask == "":
      print(Fore.RED+"internal subnet mask is empty, please try again.")
      intern_mask = input(Fore.GREEN+"Please enter internal subnet mask (ex. 255.255.255.0) ")
    print(Fore.CYAN+f"internal subnet mask = {intern_mask}")
    sysconfig(extern_nic, extern_ip, extern_mask, net_gw, intern_nic, intern_ip, intern_mask)
  ### option 3
  elif  option == 3:
    os.system('clear')
    print(Fore.GREEN+"Siptek edge proxy setting menu.")
    print()
    disp_menu()
    print()
    choice = int(input("Enter your choice: "))
    while choice != 0:
      if choice == 1:
        os.system('clear')
        print(Fore.GREEN+"Siptek edge proxy setting menu.")
        print()
        print("Choice 1 show IP-PBX ip address.")
        print()
        os.system('cat /etc/kamailio/dispatcher.list')
      elif choice == 2:
        os.system('clear')
        print(Fore.GREEN+"Siptek edge proxy setting menu.")
        print()
        print("Choice 2 add IP-PBX (doing this will restart kamailio).")
        print()
        os.system('cat /etc/kamailio/dispatcher.list')
        print()
        add_pbx = input("Please enter ip:port flags priority attributes (ex. 172.16.10.10:5060 0 0 IssabelPBX) ")
        while add_pbx == "":
          print(Fore.RED+"IP-PBX ip is empty, please try again.")
          add_pbx = input("Please enter ip:port flags priority attributes (ex. 172.16.10.10:5060 0 0 IssabelPBX) ")
        print(Fore.CYAN+f"IP-PBX ip address = {add_pbx}")
        add_pbx = "1 sip:"+add_pbx
        cmd='echo "'+add_pbx+'" >> /etc/kamailio/dispatcher.list'
        os.system(cmd)
        os.system('systemctl restart kamailio')
        print("Adding IP-PBX completed!")
      elif choice == 3:
        os.system('clear')
        print(Fore.GREEN+"Siptek edge proxy setting menu.")
        print()
        print("Choice 3 delete IP-PBX (doing this will restart kamailio).")
        print()
        os.system('cat /etc/kamailio/dispatcher.list')
        print()
        del_pbx = input("Please enter ip:port to be deleted (ex. 172.16.10.10:5060) ")
        while del_pbx == "":
          print(Fore.RED+"IP-PBX ip is empty, please try again.")
          add_pbx = input("Please enter ip:port to be deleted (ex. 172.16.10.10:5060) ")
        print(Fore.CYAN+f"IP-PBX ip address to be deleted = {del_pbx}")
        cmd = "sed -i '/"+del_pbx+"/d' /etc/kamailio/dispatcher.list"
        os.system(cmd)
        os.system('systemctl restart kamailio')
        print("Deleting IP-PBX completed!")
      else:
        os.system('clear')
        print(Fore.GREEN+"Siptek edge proxy setting menu.")
        print()
        print(Fore.RED+"Invalid choice.")
      print()
      disp_menu()
      print()
      choice = int(input("Enter your choice: "))
  ### option 4
  elif  option == 4:
    os.system('clear')
    print(Fore.GREEN+"Siptek edge proxy setting menu.")
    print()
    print("Option 4 monitor system performance.")
  else:
    os.system('clear')
    print(Fore.GREEN+"Siptek edge proxy setting menu.")
    print()
    print(Fore.RED+"Invalid option.")
  print()
  menu()
  print()
  option = int(input(Fore.GREEN+"Enter your option: "))
print()
print(Fore.GREEN+"Thanks for using siptek edge proxy. Goodbye.\n")
