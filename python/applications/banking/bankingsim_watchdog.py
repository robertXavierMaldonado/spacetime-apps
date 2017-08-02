'''
Created on July 12, 2017

@author: Robert Xavier Maldonado
'''


import logging
from datamodel.banking_sim_customers_atm.datamodel import NewRedAlertTransaction, Customer, BankingRecord
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, Setter, Deleter


logger = logging.getLogger(__name__)
LOG_HEADER = "[WATCHDOG]"


@GetterSetter(NewRedAlertTransaction, Customer)
class WatchDogSimulation(IApplication):
    """
    classdocs : this class creates a the WatchDog which proccesses all RedAlertTransactions,
                blocks the Customer that attempted to make the transaction from making any further transactions,
                and does prevents the money from moving
    """

    class WatchDog(object):
        def __init__(self):
            self.cycles = 0

        def process_transaction(self, txn, frame):
            from_c = frame.get(Customer, txn.from_c)
            from_c.block_txns()
            txn.complete_process()

    watch_dog = WatchDog()
    frame = None

    def __init__(self, frame):
        """ constructor --> used to create a frame which is use throughout the simulation """
        self.frame = frame

    def initialize(self):
        """ Nothing """
        pass
    
    def update(self):
        """ This method processes all the NewRedAlertTransaction(s),
        blocks the Customer that attempted to make the transaction from making any further transactions,
        and does prevents the money from moving
        """
        try:

            # 1 --> Get all the NewRedAlertTransaction(s)
            red_alert_txn = self.frame.get(NewRedAlertTransaction)
            #print("# of N_RA_TXNs --> " + str(len(red_alert_txn)))
            for txn in red_alert_txn:

                # 2 --> Process each RedAlert (block each customer from making transactions)
                self.watch_dog.process_transaction(txn, self.frame)

        except Exception:
            logger.exception("Error: ")

    def shutdown(self): pass
