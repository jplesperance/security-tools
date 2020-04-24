from scapy.layers import dot11
from scapy.all import sniff
import os, time
import threading
import random

hidden_bssids = {}
known_bssids = {}
channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 40, 44, 149, 153, 157, 161, 165]
clientprobes = set()

def PacketHandler(packet):

    if packet.haslayer(dot11.Dot11Beacon):
        if packet.haslayer(dot11.Dot11Elt) and packet.getlayer(dot11.Dot11FCS).addr2:
            ssid = packet.getlayer(dot11.Dot11Elt).info

            if ssid == '' or packet.getlayer(dot11.Dot11Elt).ID != 0:
                if not hidden_bssids.has_key(ssid):
                    print("Hidden Network", packet.getlayer(dot11.Dot11FCS).addr2)
                    hidden_bssids[ssid] = packet.getlayer(dot11.Dot11FCS).addr2
            else:
                if not known_bssids.has_key(ssid):
                    print("Network Detected: %s at %s" % (ssid, packet.getlayer(dot11.Dot11FCS).addr2))
                    known_bssids[ssid] = packet.getlayer(dot11.Dot11FCS).addr2
    if packet.haslayer(dot11.Dot11ProbeResp) and (packet.addr3 in hidden_bssids.values()):
        print("Hidden SSID Uncovered! ", packet.info, packet.addr3)
    if packet.haslayer(dot11.Dot11ProbeReq):
        if len(packet.info) > 0:
            testcase = packet.addr2 + '---' + packet.info
            if testcase not in clientprobes:
                clientprobes.add(testcase)
                print("New Probe Found: " + packet.addr2 + ' ' + packet.info)
                print("\n---------------Client Probes Table---------------\n")
                counter = 1
                for probe in clientprobes:
                    [client, ssid] = probe.split('---')
                    print(counter, client, ssid)
                    counter += 1
                print("\n--------------------------------------------------\n")

def hopper(iface):
    n = 1
    g = 1
    stop_hopper = False
    while not stop_hopper:
        g += 1
        if g == 2000:
            stop_hopper = True
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))

        dig = int(random.choice(channels))
        if dig != 0 and dig != n:
            n = dig
    print("")
    print("")
    print("Known Networks Logged")
    print("")
    for key,value in known_bssids.items():
        print(key, value)
    print("")
    print("Hidden Networks Logged")
    print("")
    for key, value in hidden_bssids.items():
        print(key, value)
    print("")
    print("Client Probes Logged")
    print("")
    for line in clientprobes:
        print(line)
    exit(0)

if __name__ == "__main__":
    thread = threading.Thread(target=hopper, args=('wlan0mon', ), name="hopper")
    thread.daemon = True
    thread.start()
    sniff(iface = "wlan0mon", prn=PacketHandler)