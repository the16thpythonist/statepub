# Third party library imports
import psutil


class StateInterface:
    """
    This is the Interface for any new "Sate" object.
    The state objects are meant to describe some sort of current state/value of either the Computer as a whole, a sort
    of Process etc.
    A specific state object has a fixed set of values it represents. How these values are read from the system will be
    hardcoded into them. But the method, which starts this process of getting all the necessary values will have to be
    the same. "acquire" will update the object internal attributes of the object.
    The method "to_dict" will have to return a dictionary of all the values, that are represented by the state object.
    This is necessary to later publish them to their respective MQTT topics. The topic names (at least at the top level)
    will have the same names as the attributes of the state objects.

    CHANGELOG

    Added 28.12.2018
    """
    def acquire(self):
        """
        This method will get called to get the current(!) state of whatever value is being described by the specific
        state class/object and update all the attributes of the object.

        CHANGELOG

        Added 28.12.2018
        :return:
        """
        raise NotImplementedError()

    def to_dict(self):
        """
        This method will return a dictionary, whose keys are the names which the MQTT topics are supposed to have when
        publishing and the values are the values, which are supposed to be published to the MQTT system.

        This is not supposed to call the "acquire" method. This method will merely create a dict from whatever
        information about the values is currently at the disposal of the object.

        CHANGELOG

        Added 28.12.2018

        :return:
        """
        raise NotImplementedError()


class ComputingState(StateInterface):

    def __init__(self):
        self.attributes = {
            'cpu':  '0.0',
            'ram':  '0.0'
        }

    def acquire(self):
        # Getting the CPU usage as a percentage. The interval=1 makes a blocking call, that observes the CPU usage for
        # one second. The percpu=False makes it so
        # that only a single value is returned, which will be the average over all the cores.
        self.attributes['cpu'] = psutil.cpu_percent(interval=1, percpu=False)

        # Getting the memory stats of the machine. The function actually returns a whole bunch of info. But here we are
        # just using the percentage of used RAM as a indicator. This value is stored in the percent attribute of the
        # returned wrapper object.
        self.attributes['ram'] = psutil.virtual_memory().percent

    def to_dict(self):
        return self.attributes

    @property
    def cpu(self):
        return self.attributes['cpu']

    @property
    def ram(self):
        return self.attributes['ram']


class NetworkState(StateInterface):

    def __init__(self):
        self.attributes = {
            'bytes_sent': '0',
            'bytes_recv': '0',
        }

    def acquire(self):
        # This function will return the wrapper object which contains all the network statistics
        network_stats = psutil.net_io_counters()

        self.attributes['bytes_sent'] = network_stats.bytes_sent
        self.attributes['bytes_recv'] = network_stats.bytes_recv

    def to_dict(self):
        return self.attributes

    @property
    def bytes_sent(self):
        return self.attributes['bytes_sent']

    @property
    def bytes_recv(self):
        return self.attributes['bytes_recv']
