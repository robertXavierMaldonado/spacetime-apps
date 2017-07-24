'''
Created on June 30, 2017

@author: Robert Xavier Maldonado
'''

import logging
from random import choice
from datamodel.banking_sim_customers_atm.datamodel import Customer, Transaction, CustomerView
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, Getter

logger = logging.getLogger(__name__)
LOG_HEADER = "[CUSTOMER]"


@Producer(Transaction, Customer)
@Getter(CustomerView)
class CustomerSimulation(IApplication):
    """
    classdocs : this class creates a the Customer Simulation by creating a Customer and randomizing the Customer's
                Transaction
    """

    frame = None  # stores the frame that is used throughout the simualtion


    def __init__(self, frame):
        """
        constuctor -> used to create a frame -> this frame is used throughout the simulation
        """
        self.frame = frame

    def initialize(self):
        """
        Creates one randomized customer object representing itself
        """
        customer_num = 250
        for i in range(customer_num):  # Create a bumch of Customer objects in spacetime, this will be used in the simulation
            self.frame.add(Customer())  # This one object goes to the spacetime server table

    def update(self):
        """
        gets all CustomerView objects, picks one at random, and makes one random transaction to that person
        """

        try:
            customers = self.frame.get(Customer)

            rdm_cus = choice(customers)

            customer_views = self.frame.get(CustomerView)

            customer_view = None
            for c in customer_views:
                if c.give_account_number() == rdm_cus.give_account_number():
                    customer_view = c
                    break

            # print("\n(CUSTOMER VEW) --> " + str(customer_view))

            new_txn = Transaction(rdm_cus)
            # print("TXN :::::::: " + str(new_txn))

            self.frame.add(new_txn)

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass


'''
@GetterSetter(Customer)
@Producer(Customer)
class CustomerSimulation(IApplication):
    """
    classdocs : this class creates a the Customer Simulation by creating a Customer and randomizing the Customer's
                Transaction
    """

    frame = None
    customer = None  # used to contain the customer



    def __init__(self, frame):
        """
        constuctor -> used to create a frame -> this frame is used throughout the simulation
        """
        self.frame = frame

    def initialize(self):
        """
        This method will initilize the simulation, creating one customer
        """
        new_customer = Customer()
        self.frame.add(new_customer)  # This one object goes to the spacetime server list and stays there
        self.customer = new_customer

        # logger.debug("%s ************** CUSTOMERS IN FRAME %s", LOG_HEADER, self.customer)

    def update(self):
        """ This method will be called to run the transaction on one customer, removes that customer, then adds a new
            one for the next cycle
        """
        # logger.info("%s Update", LOG_HEADER)
        # logger.debug("%s Customer :::: \n%s", LOG_HEADER, self.customer[0])
        # logger.debug("%s Customer Action Compelete? :::: %s", LOG_HEADER, self.customer[0].give_Competed())

        try:
            # print(self.customer)
            # print("- " * 65)
            self.customer.randomize_Transaction()
            # print(self.customer)
            # print("\n" + "#" * 25 + "\n")

        except Exception:
            logger.exception("Error: ")

    def shutdown(self):
        pass
'''
