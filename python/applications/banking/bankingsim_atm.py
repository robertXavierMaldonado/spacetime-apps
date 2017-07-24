'''
Created on June 30, 2017

@author: Robert Xavier Maldonado
'''

import logging
from datamodel.banking_sim_customers_atm.datamodel import NewValidTransaction, NewRedAlertTransaction, BankingRecord
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, Setter, Deleter

logger = logging.getLogger(__name__)
LOG_HEADER = "[ATM]"


@Producer(BankingRecord)
@Deleter(NewValidTransaction, NewRedAlertTransaction)
@GetterSetter(NewValidTransaction, NewRedAlertTransaction)
class ATMSimulation(IApplication):
    """
    classdocs : this class creates an ATM Simulation which runs the transactions of all customers stored in spacetime
                additionally, the simulation records all transactions on ecah customer's Banking Record
    """

    class ATM:
        def __init__(self):
            self.valid_txn_count = 0
            self.redaler_txn_count = 0
            self.storage = 0

        def make_transaction(self, txn_type, amount):
            if txn_type == "W":
                self.storage -= amount
            elif txn_type == "D":
                self.storage += amount

        def count_txn(self, txn_valid):
            if txn_valid:
                self.valid_txn_count += 1
            elif not txn_valid:
                self.redaler_txn_count += 1

        def print_data(self):
            print("(ATM DATA) ------> [$ : {}] - [V TXN # : {}] - [RA TXN # : {}]".format(str(self.storage), str(self.valid_txn_count), str(self.redaler_txn_count)))

    frame = None

    new_valid_txns = []
    new_redalert_txns = []
    banking_records = []

    atm = ATM()


    def __init__(self, frame):
        """
        constructor -> used to create a frame which is use throughout the simulation
        """
        self.frame = frame

    def initialize(self):
        """
        Nothing
        """
        pass

    def update(self):
        """
        1) Get a validTransaction, update both the customer bank records with the right values
        2) Get all RedAlertTransaction and block the transaction (print out an alert for this)
        """
        print("\n")
        try:

            # Process all the NewValidTransactions
            self.new_valid_txns = self.frame.get(NewValidTransaction)
            if self.new_valid_txns:
                for txn in self.new_valid_txns:

                    # Make the transaction with the ATM & count it
                    self.atm.make_transaction(txn.give_type(), txn.give_amount())
                    self.atm.count_txn(True)

                    # Make a banking record or the txn and add it
                    new_banking_record = BankingRecord(txn)
                    record = new_banking_record.give_Record()
                    record += new_banking_record.give_Record() + [{"CUSTOMER ACC NO": txn.give_customer_an(), "TXN TYPE": txn.give_type(), "TXN AMOUNT": txn.give_amount()}]
                    self.frame.add(new_banking_record)

                    # Compelete the process and delete it
                    txn.complete_process()
                    self.frame.delete(NewValidTransaction, txn)

                    # Print confimation
                    print("(CUSTOMER TXN) --> [COMPLETE]")
            else:
                pass
                # print("NN [VALID] TXN")

            # Process all the NewRedAlertTransaction
            self.new_redalert_txns = self.frame.get(NewRedAlertTransaction)
            if self.new_redalert_txns:
                for ra_txn in self.new_redalert_txns:

                    # Count the txn
                    self.atm.count_txn(False)

                    # Compelete the process and delete it
                    ra_txn.complete_process()
                    self.frame.delete(NewRedAlertTransaction, ra_txn)

                    # Print Block comfirmation
                    print("(CUSTOMER TXN) --> [BLOCKED]")
            else:
                pass
                # print("NN [RED A] TXN")

            self.atm.print_data()

            # Look at the BankingRecords nand print them
            # self.banking_records = self.frame.get(BankingRecord)
            # print("BANKING RECORD COUNT: " + str(len(self.banking_records)))
            # for br in self.banking_records:
            #     print(br.return_formated_records())

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass


'''
@Producer(ATM, BankingRecord)
@GetterSetter(ATM, BankingRecord, ValidCustomer, InvalidCustomer, Customer)
class ATMSimulation(IApplication):
    """
    classdocs : this class creates an ATM Simulation which runs the transactions of all customers stored in spacetime
                additionally, the simulation records all transactions on ecah customer's Banking Record
    """

    frame = None
    atm = None
    cycle_count = 0
    banking_records = []
    valid_customers = []

    def __init__(self, frame):
        """
        constructor -> used to create a frame which is use throughout the simulation
        """
        self.frame = frame

    def initialize(self):
        """
        This method will initiate the ATM simulation, creating one ATM and a Banking Record
        """
        new_atm = ATM()
        self.frame.add(new_atm)
        self.atm = new_atm

        # new_record = BankingRecord()
        # self.frame.add(new_record)
        # self.record = new_record

    def update(self):
        """
        This method will be called to run the transactions of all Valid Customers on the ATM
        """
        try:

            #  Creates BankingRecords for new Customers added to spacetime

            for new_customer in self.frame.get_new(ValidCustomer):
                new_record = BankingRecord(new_customer)
                self.frame.add(new_record)

            self.cycle_count += 1
            self.valid_customers = self.frame.get(ValidCustomer)
            self.banking_records = self.frame.get(BankingRecord)

            if self.valid_customers:
                for customer in self.valid_customers:
                    if not customer.give_Completed():

                        single_log = self.atm.execute_Transaction(customer)
                        c_record = self.frame.get(BankingRecord, customer.give_ID())

                        if type(c_record) == list:
                            # print('here +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=')
                            c_record = c_record[0]
                            c_record.Record.append(single_log)  # reassing the c_record.Record to a new value, Record = Record + []
                        else:
                            c_record.Record.append(single_log)

            # Prints stuff in the console
            if self.cycle_count % 2 == 0:
                # print("\n" + "Banking Record --> [Cycle : " + str(self.cycle_count/2) + "] <-----------------------------------------------------------------------------------------")
                # print("[Bank $ : " + str(self.atm.give_Storage()) + "]")
                # print("[Valid Customer Count : " + str(len(self.valid_customers)) + " ]")

                print("\n** ATM SIMULATION **")
                # print(self.banking_records)
                for r in self.banking_records:
                    print(r)

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass

'''