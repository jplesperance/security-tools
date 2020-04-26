import os
import random
import threading
import time

import click
from scapy.all import sniff
from scapy.layers import dot11


class Parse(object):
    thread = threading.Thread()
    hidden_bssids = []
    known_bssids = {}
    probesResp = {}
    channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 36, 40, 44, 149, 153, 157, 161, 165]
    clientprobes = set()
    length = 300
    known = False
    hidden = False
    probes = 'none'
    discover_hidden = False
    write = "scan"
    interface = "wlan0mon"

    def __init__(self, length, known, hidden, probes, discover_hidden, write, interface):
        print(length, known, hidden, probes, discover_hidden, write, interface)
        self.length = length
        if known:
            self.known = known
        if hidden:
            self.hidden = hidden
        if discover_hidden:
            self.discover_hidden = discover_hidden
        if write:
            self.write = write
        self.probes = probes
        self.interface = interface

        sniff(iface=self.interface, prn=self.PacketHandler)

    def PacketHandler(self, packet):
        if packet.haslayer(dot11.Dot11Beacon):
            if packet.haslayer(dot11.Dot11Elt) and packet.getlayer(dot11.Dot11FCS).addr2:
                ssid = packet.getlayer(dot11.Dot11Elt).info
                if self.hidden:
                    if ssid.decode() == '':
                        if packet.addr2 not in self.hidden_bssids:
                            self.hidden_bssids.append(packet.getlayer(dot11.Dot11FCS).addr3)

                if self.known:
                    if ssid.decode() != '' or packet.getlayer(dot11.Dot11Elt).ID == 'SSID':
                        if ssid.decode() not in self.known_bssids.keys():
                            self.known_bssids[ssid.decode()] = packet.getlayer(dot11.Dot11FCS).addr3
        if self.discover_hidden:
            if packet.haslayer(dot11.Dot11ProbeResp):
                self.probesResp[packet.addr2] = packet.info.decode()
        if self.probes == 'all' or self.probes == 'unknown':
            if packet.haslayer(dot11.Dot11AssoReq):
                if len(packet.info) > 0:
                    testcase = packet.addr2 + '---' + str(packet.info)
                    if self.probes == 'all':
                        if testcase not in self.clientprobes:
                            self.clientprobes.add(testcase)

                    else:
                        if testcase not in self.clientprobes:
                            if packet.info.decode() not in self.known_bssids.keys():
                                self.clientprobes.add(testcase)


def hopper(iface, length, known, hidden, probes, discover_hidden, write):
    n = 1
    g = 1
    stop_hopper = False
    while not stop_hopper:
        if g % 60 == 0:
            print(int(g / 60))
        g += 1
        if g == length * 2:
            stop_hopper = True
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))

        dig = int(random.choice(Parse.channels))
        if dig != 0 and dig != n:
            n = dig
    if not write:
        write = "scan"
    if known:
        print("Writing Found SSIDs to file: " + write + "_ssids.csv")
        f = open(write + "_ssids.csv", 'w')
        for key, value in Parse.known_bssids.items():
            f.write(key + "," + value + "\n")
        f.close()
    if hidden:
        print("Writing Hidden Networks to file: " + write + "_ssids.csv")
        f = open(write + '_hidden.csv', 'w')
        for line in Parse.hidden_bssids:
            f.write(line + "\n")
        f.close()

    if probes != 'none':
        print("Writing " + probes + " client probes to file: " + write + "_ssids.csv")
        f = open(write + "_probes.csv", 'w')
        for line in Parse.clientprobes:
            f.write(line + "\n")
        f.close()

    if discover_hidden:
        print("Writing Discovered Hidden SSIDs to file: " + write + "_ssids.csv")
        f = open(write + "_discovered", 'w')
        for key, value in Parse.probesResp.items():
            if key in Parse.hidden_bssids:
                f.write(value + "," + key + "\n")
        f.close()
    return


@click.command(help='Capture various wifi information')
@click.option('-t', '--time', 'length', type=click.INT, default=300, help='lenfth in seconds to run the capture for',
              show_default=True)
@click.option('-k', '--known', is_flag=True, help='Log broadcasted SSIDs')
@click.option('-h', '--hidden', is_flag=True, help='Log hidden access points')
@click.option('-p', '--probes', type=click.Choice(['none', 'all', 'unknown']), default='none',
              help='Capture no probes, all probes or just probes for unknown networks', show_default=True)
@click.option('-d', '--discover-hidden', is_flag=True, help='Discover SSIDs for hidden networks')
@click.option('-w', '--write', type=click.STRING, help='enable writing findings to file')
@click.option('-i', '--interface', type=click.STRING, default='wlan0mon', show_default=True)
def cli(length, known, hidden, probes, discover_hidden, write, interface):
    thread = threading.Thread(target=hopper, args=(interface, length, known, hidden, probes, discover_hidden, write))
    thread.daemon = True
    thread.start()
    Parse(length, known, hidden, probes, discover_hidden, write, interface)


if __name__ == '__main__':
    cli()
