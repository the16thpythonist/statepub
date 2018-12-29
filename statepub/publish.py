# Std library imports
import os
import time
# Third party imports
import paho.mqtt.client as mqtt
# in-package imports
from statepub.state import StateInterface


class StatePublisher:

    # The mqtt client object expects an ID. This static field will keep track of how many Publisher objects have been
    # created and supplies each one with a new ID.
    id_counter = 0

    def __init__(self, topic_base, broker_ip, broker_port=1883):
        self.topic_base = topic_base

        # We get the ID of the current object by using the current state of the static id counter which always provides
        # a new unique integer ID. then of course we have to increment that so that the next object to be created will
        # also have a unique ID.
        self.id = StatePublisher.id_counter
        StatePublisher.id_counter += 1
        print(self.id_counter)

        # We need to create a MQTT client object, which we will store as a attribute of the publisher object, so it can
        # be used in every method.
        self.client = mqtt.Client("Publisher{}".format(self.id))

        # Now we just need to connect the client to the broker(server) and it is ready to go.
        self.client.connect(broker_ip, broker_port)
        self.client.loop_start()

    def publish(self, *states, topic=''):

        # What we do here is we get the dictionary representations of all states and then merge them together into one
        # big dictionary and then call the method which publishes the dictionary.
        combined_dict = {
            'timestamp': time.time()
        }
        for state in states:  # type: StateInterface

            # Obviously we want the new state information, so we call the acquire on each of the states
            state.acquire()
            combined_dict.update(state.to_dict())

        self.publish_dict(combined_dict, topic)

    def publish_dict(self, dictionary, topic):

        for key, value in dictionary.items():
            # Creating the topic to publish the value to by joining the actual name of the topic, which is the key
            # string in this dict with the base path given to the publisher object and the base path given to this
            # method
            topic_string = os.path.join(self.topic_base, topic, key)

            self.client.publish(topic_string, str(value))

    def close(self):
        self.client.disconnect()
        self.client.loop_stop()
