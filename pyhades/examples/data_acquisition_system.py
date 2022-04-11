r"""
pyhades/examples/data_acquisition_system.py

This module explains how to implement a data acquisition system
"""

from pyhades import PyHades, PyHadesStateMachine, State
from pyhades.tags import CVTEngine, TagBinding
import requests
import os
import logging

# PyHades app definition
app = PyHades()
app.set_mode('Development')
app.set_db(dbfile="app.db")

# Tag Definitions
tag_engine = CVTEngine()
tag_engine.set_tag('Triangle', 'Adim.', 'int', 'Simulator triangle variable', -1, 1)

# Tag Definition on DB
interval = 1.0
app.set_dbtags(['Triangle'], interval)

@app.define_machine(name='DAS', interval=1.0, mode="async")
class DAS(PyHadesStateMachine):

    # State Definitions
    starting = State('Starting', initial=True)
    running = State('Running')

    # Transitions Definitions
    starting_to_running = starting.to(running)

    # Parameters
    triangle_var = TagBinding('Triangle', direction='write')

    def __init__(self, name):

        super().__init__(name)

    def while_starting(self):

        client_id = None
        self.opcua_client_url = "http://localhost:8001"
        # OPC_SERVER_URL = "opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer"
        self.opcua_server_url = os.environ.get('OPC_SERVER_URL')

        # Connect with opcua server
        payload = {'url': self.opcua_server_url}
        response = requests.post(f'{self.opcua_client_url}/api/client/connect_to_server', json=payload)
        response = response.json()

        if response['is_connected']:
            
            client_id = response['id']

            self.client_id = client_id

            self.triangle_node_id = "ns=3;i=1006"

            self.starting_to_running()

    def while_running(self):

        # Reading Triangle Variable from opc ua client
        payload = {
            "namespace": self.triangle_node_id,
            "client_id": self.client_id
        }
        response = requests.post(f"{self.opcua_client_url}/api/client/node_attributes", json=payload)
        response = response.json()

        # Writing to Data Acquisition system Database (SQLite) for this demo
        self.triangle_var = response["Value"]

    def disconnect_opc_client(self):

        try:
            url = f'{self.opcua_client_url}/api/client/disconnect/{self.client_id}'
            response = requests.get(url)
            resp = response.json()

            logging.info(f"Machine - {self.name}: {resp['message']}")
        except Exception as e:
            error = str(e)
            logging.error(f"Machine - {self.name}:{error}")


if __name__=="__main__":

    try: 
            
        app.run()

    except (KeyboardInterrupt, SystemExit):
        
        das = app.get_machine('DAS')
        das.disconnect_opc_client()
    