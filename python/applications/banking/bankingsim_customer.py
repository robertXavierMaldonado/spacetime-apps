'''
Created on June 30, 2017

@author: Robert Xavier Maldonado
'''

import logging
from random import choice
from datamodel.banking_sim_customers_atm.datamodel import Customer, Transaction, CustomerView
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, Getter, Setter, GetterSetter

logger = logging.getLogger(__name__)
LOG_HEADER = "[CUSTOMER]"


@Getter(CustomerView)
@Producer(Transaction, Customer)
class CustomerSimulation(IApplication):
    """ classdocs : this class creates a the Customer Simulation by creating a Customer and randomizing the Customer's Transaction """

    frame = None  # stores the frame that is used throughout the simualtion
    customer = None # stores this simulation's Customer Object

    def __init__(self, frame):
        """ constuctor : used to create a frame -> this frame is used throughout the simulation """
        self.frame = frame

    def initialize(self):
        """ Creates one randomized customer object representing itself """
        self.customer = Customer()
        self.frame.add(self.customer)  # This one object goes to the spacetime server, this will be used in the simulation\

    def update(self):
        """
        1) Checks txn type, if "T": gets all Customer objects, picks one at random (which is not self.customer)
        2) self.customer makes one random transaction to randomly chosen person
        3) the txn_amount of self.customer is randomized """

        self.customer = self.frame.get(Customer, self.customer.account_number) # Update the self.Customer
        customers = None
        new_txn = None

        try:

            # Checks if the customer is able to make transactions, this is set to False by WatchDog
            if self.customer.can_make_txn:

                # 1 --> Only find another customer if self.customer is making a transaction to another Customer
                if self.customer.txn_type == "T":
                    
                    customers = self.frame.get(CustomerView) # customers that are randomly selected from
                    rdm_cus = choice(customers) # rdm selected customer

                    # this process is to ensure the random customer is not the same as self.customer (customer cannot transfer money to self)
                    while rdm_cus == self.customer:
                        rdm_cus = choice(customers)

                else:
                    rdm_cus = None

                # 2 --> Create a new Transaction, Add the new Transaction Object to spacetime
                new_txn = Transaction(self.customer, rdm_cus)
                self.frame.add(new_txn)

                # 3 --> randomize self.customer's txn values so the customer doesn't continue to make txns with the same values
                self.customer.randomize_txn_values()

            else:
                #print("# CUSTOMER " + str(self.customer.account_number) + " BLOCKED FROM MAKING TRANSACTIONS #")
                pass

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass
