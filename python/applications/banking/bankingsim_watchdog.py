'''
Created on July 12, 2017

@author: Robert Xavier Maldonado
'''


#      #
#      #
#      #
#  NOT #
#  IN  #
#  USE #
#      #
#      #
#      #


import logging
from datamodel.banking_sim_customers_atm.datamodel import ValidCustomer, BankingRecord, Customer
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, Setter, Deleter

logger = logging.getLogger(__name__)
LOG_HEADER = "[WATCHDOG]"

@Producer(ValidCustomer, BankingRecord, Customer)
@GetterSetter(ValidCustomer, BankingRecord, Customer)
class WatchDogSimulation(IApplication):
    """
    classdocs : this class creates a the Watch Dog Simulation that searches the banking history of customers and flags
                them if they are suspicuous
                supicuous = customer's transaction amount is < 1,000,000
    """

    frame = None
    banking_records = []

    def __init__(self, frame):
        self.frame = frame

    def initialize(self):
        self.banking_records = self.frame.get(BankingRecord)

    def update(self):
        try:

            self.banking_records = self.frame.get(BankingRecord)
            print("\n** WATCHDOG SIMULATION ** ")
            # print(self.banking_records)
            for r in self.banking_records:
                print(r)
                # print(type(r.Record), r.Record)

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass


