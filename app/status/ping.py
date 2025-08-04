import xml.etree.ElementTree as ET
import os
import re
import subprocess
import time

import ipinfo
import requests

from app.ev import EV

geo_cache:dict = {}

def get_request(url: str):
    if not re.search('[a-zA-Z]', url): # if string does not contain letters (not a domain name)
        return
    url = "http://" + url
    response = requests.get(url=url)
    if response.status_code == 200:
        return True

def ping(host) -> bool:
    param = '-n' if 'nt' in os.name.lower() else '-c'
    command = ['ping', param, '1', host]
    
    # keep the output quiet (varies depending on the OS) 
    if 'nt' in os.name.lower():
        command.extend(['>', 'nul', '2>&1'])
    else:
        command.extend(['>', '/dev/null', '2>&1'])

    # Join the command list into a single string for subprocess.call
    command_str = ' '.join(command)

    time.sleep(0.5)

    if subprocess.call(command_str, shell=True) == 0:
        return True
    # some servers don't allow pings. if we have a domain name, try to make a regular GET request instead
    if get_request(url=host):
        return True

def geolocation(ip: str) -> str:
    '''
    the service we use to retreive this data rate limits us. since IP addresses
    tend not to change too much, we can safely cache the values. We're
    only caching to a global variable, so every time you restart the program (redeploy),
    the cache is emptied.
    '''
    try:
        token = EV().IPInfoToken
        if ip in geo_cache:
            return geo_cache.get(ip)
        handler = ipinfo.getHandler(token)
        details = handler.getDetails(ip)
        location = f"{details.city} ({details.region})"
        geo_cache.update({ip: location})
        return location
    except:
        # if we've exceeded our request limit for the month
        return "geolocation?"

class Icecast:
    def __init__(self) -> None:
        self.icecast_URL = "http://npl.streamguys1.com:/admin/stats.xml"
        self.ev = EV()
        self.icecast_tree = self.get_tree()
        self.mount_list = self.get_mount_list()
        self.mounts = self.check_mounts()
        self.listeners = self.get_listeners()
        self.server_start = self.get_server_start()
        self.outgoing_kbitrate = self.get_outgoing_kbitrate()
        self.sources = self.get_sources()

    def get_tree(self) -> ET.ElementTree:
        tree = requests.get(self.icecast_URL, auth=(self.ev.icecast_user, self.ev.icecast_pass))
        tree = tree.text
        tree = ET.fromstring(tree)
        return tree
    
    def get_mount_list(self) -> list:
        mount_list = []
        tree = self.icecast_tree
        try:
            mountpoints = tree.findall("source")
            for mount in mountpoints:
                mount = mount.get("mount")
                mount_list.append(mount)
        except:
            mount_list.append("cannot get mounts")
        return mount_list

    def check_mounts(self) -> list:
        mount_list = []
        tree = self.icecast_tree
        mountpoints = tree.findall('source')
        for mount in mountpoints:         
            # Not all mounts have all the same data. This is a little messy but it's (perhaps) the easiest way to do it   
            mount_list.append( 
                    {"name": mount.get('mount'),
                    "stream_start":  mount.find("stream_start").text if mount.find("stream_start") != None else "-",
                    "listeners": mount.find("listeners").text if mount.find("listeners") != None else "-",
                    "incoming_bitrate": round(int(mount.find("incoming_bitrate").text)/1000, 0) if mount.find("incoming_bitrate") != None else "-",
                    "outgoing_kbitrate": mount.find("outgoing_kbitrate").text if mount.find("outgoing_kbitrate") != None else "-",
                    "title": mount.find("title").text if mount.find("title") != None else "-",
                    "metadata_updated": mount.find("metadata_updated").text if mount.find("metadata_updated") != None else "-",
                    "listenurl": mount.find("listenurl").text if mount.find("listenurl") != None else "-"
                    }
                )

        return mount_list

    def get_listeners(self) -> str:
        tree = self.icecast_tree
        listeners = tree.find('listeners').text
        return listeners

    def get_server_start(self) -> str:
        tree = self.icecast_tree
        server_start = tree.find('server_start').text
        return server_start

    def get_outgoing_kbitrate(self) -> str:
        tree = self.icecast_tree
        bitrate = tree.find('outgoing_kbitrate').text
        return bitrate
    
    def get_sources(self) -> str:
        tree = self.icecast_tree
        sources = tree.find("sources").text
        return sources

    def user_agent_ip(self, mount) -> list:
        icecast_URL = f"http://npl.streamguys1.com:/admin/listclients?mount=/{mount}"
        tree = requests.get(icecast_URL, auth=(self.ev.icecast_user, self.ev.icecast_pass))
        tree = tree.text
        tree = ET.fromstring(tree)
        mountpoint = tree.find('source')
        agents = []
        try:
            listeners = mountpoint.findall('listener')
            for listener in listeners:
                IP_address = listener.find("IP").text
                geo = geolocation(ip=IP_address)

                user_agent = listener.find('UserAgent').text

                connected = listener.find("Connected").text
                connected = str(round(int(connected) / 60, 1)) # convert to minutes, round to one decimal

                agents.append(f" {IP_address} • {geo} • {user_agent} • {connected} minutes")
            return agents
        except:
            return agents