
import psutil

from statepub.state import ComputingState
from statepub.state import NetworkState


def try_computing_state():
    cs = ComputingState()
    cs.acquire()
    print('THE CPU USAGE "{}"\nTHE RAM USAGE "{}"'.format(cs.cpu, cs.ram))


def try_network_state():
    ns = NetworkState()
    ns.acquire()
    print('BYTES SENT "{}"\nBYTES RECEIVED "{}"'.format(ns.bytes_sent, ns.bytes_recv))


#try_computing_state()
try_network_state()
