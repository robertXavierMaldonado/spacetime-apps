'''
Created on June 30, 2017

@author: Robert Xavier Maldonado
'''

import logging
from datamodel.banking_sim_customers_atm.datamodel import NewValidTransaction, BankingRecord, Customer
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, Setter, Deleter

logger = logging.getLogger(__name__)
LOG_HEADER = "[ATM]"


@Producer(BankingRecord)
@GetterSetter(Customer, BankingRecord, NewValidTransaction)
class ATMSimulation(IApplication):
    """
    classdocs : this class creates an ATM Simulation which runs the transactions of all customers stored in spacetime
                additionally, the simulation records all transactions on ecah customer's Banking Record
    """

    class ATM(object):
        def __init__(self):
            self.storage = 0
            self.cycles = 0

        def process_transaction(self, txn, frame):
            self.cycles += 1
            customer = frame.get(Customer, txn.from_c) # get the Customer that initiated txn

            if txn.txn_type == "W":
                self.storage -= txn.txn_amount # sub (amount) from the ATM
                customer.balance += txn.txn_amount # add (amount) to the Customer

            elif txn.txn_type == "D":
                self.storage += txn.txn_amount # add (amount) to the ATM
                customer.balance -= txn.txn_amount # sub (amount) from the Customer 

            elif txn.txn_type == "T":
                to_customer = frame.get(Customer, txn.to_c) # Get the Customer that will recieve (amount)
                customer.balance -= txn.txn_amount # sub (amount) from Customer that made the transaction
                to_customer.balance += txn.txn_amount # add (amount) to the revieving Customer

            txn.complete_process()

        def update_banking_record(self, txn, frame):

            try: # Check if there is a BankingRecord for this Customer already in spacetime
                pre_txn_rec = frame.get(BankingRecord, txn.from_c)
                pre_txn_rec.update_record(txn) # Update the record according to the record


            except Exception: # If not, then make one
                frame.add(BankingRecord(txn))

        def print_using_base(self, base, frame, type):
            if type == BankingRecord:
                if self.cycles%base == 0:
                    master_string = "B_RECORDS --> c:" + str(self.cycles/base) + " <------------------------------------------------------------------------------------------------------\n"
                    for r in frame.get(BankingRecord):
                        master_string += r.return_formated_records()
                    print(master_string)
            elif type == Customer:
                if self.cycles%base == 0:
                    master_string = "CUSTOMERS --> c:" + str(self.cycles/base) + " <------------------------------------------------------------------------------------------------------\n"
                    for c in frame.get(Customer):
                        master_string += str(c) + "\n"
                    print(master_string)    


    atm = ATM()
    frame = None

    def __init__(self, frame):
        """ constructor --> used to create a frame which is use throughout the simulation """
        self.frame = frame

    def initialize(self):
        """ Nothing """
        pass

    def update(self):
        """ This method processes all the NewValidTransaction(s) and creates BankingRecords for each Transaction """
        try:

            # 1 --> Get all the NewValidTransaction(s)
            new_valid_txns = self.frame.get(NewValidTransaction)

            for txn in new_valid_txns:

                # 2 --> Update the BankingRecord corresponding to Customer that initiated it
                self.atm.update_banking_record(txn, self.frame)

                # 3 --> Process the Transaction 
                self.atm.process_transaction(txn, self.frame)

                # ~ Print based on a cycle count (optional functionality)
                self.atm.print_using_base(10, self.frame, Customer)
                #self.atm.print_using_base(10, self.frame, BankingRecord)

        except Exception:
            logger.exception("Error: ")

    def shutdown(self): pass
