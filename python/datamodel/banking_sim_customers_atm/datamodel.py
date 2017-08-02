"""
Created on June 28, 2017

@author: RobertXavierMaldonado
"""


from __future__ import absolute_import
from random import randrange, choice
import logging
from pcc.join import join
from pcc.subset import subset
from pcc.parameter import parameter, ParameterMode
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey


import uuid
import traceback


logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"


@pcc_set
class Customer(object):
    """Class for modelling a customer from a Bank's point of view"""

    # key --> spacetime key for Customer object
    @primarykey(str)
    def account_number(self): return self.__account_number
    @account_number.setter
    def account_number(self, v): self.__account_number = v
       
    # balance --> money stored by the customer
    @dimension(int)
    def balance(self): return self.__balance
    @balance.setter
    def balance(self, v): self.__balance = v
       
    # txn_amount --> random amount that customer want's to transfer in a txn
    @dimension(int)
    def txn_amount(self): return self.__txn_amount
    @txn_amount.setter
    def txn_amount(self, v): self.__txn_amount = v
       
    # can_make_txn --> bool that allows the customer to make txns
    @dimension(bool)
    def can_make_txn(self): return self.__can_make_txn
    @can_make_txn.setter
    def can_make_txn(self, v): self.__can_make_txn = v

    # txn_type --> "W" = Withdraw, "D" = Deposit, "T" = Transfer
    @dimension(str)
    def txn_type(self): return self.__txn_type
    @txn_type.setter
    def txn_type(self, v): self.__txn_type = v
    
    # randomize the values of txn_amount and txn_type
    def randomize_txn_values(self):
        self.txn_amount = randrange(1, 1050000)
        self.txn_type = choice(["W", "D", "T"])

    # name --> int representing name of Customer (will eventually change to actual names)
    #@dimension(str)
    #def name(self): return self.__name
    #@name.setter
    #def name(self, v): self.__name = v

    def block_txns(self): self.can_make_txn = False

    def __init__(self):
        self.balance = 10000000
        self.randomize_txn_values()
        self.can_make_txn = True
        #self.name = randrange(1, 999)

    def __str__(self):
        return "[ACC_NO : {:s}] - [CM TXN : {:s}] - [TXN_TYPE : {:s}] - [BAL : {:9d}] - [TXN_AM : {:7d}]".format(
            str(self.account_number), str(self.can_make_txn), str(self.txn_type), self.balance, self.txn_amount)


@projection(Customer, Customer.account_number, Customer.balance)
class CustomerView(Customer):
    """ Class for modelling the what the customeer is allowed to view """

    def __str__(self):
        return "[ACC_NO : {:s}] - [BAL : {:9d}]".format(str(self.account_number), self.balance)


@pcc_set
class Transaction(object):
    """A trasaction made by the customer"""

    # txn_id --> spacetime key for Transaction object
    @primarykey(str)
    def txn_id(self): return self.__txn_id
    @txn_id.setter
    def txn_id(self, v): self.__txn_id = v

    # txn_amount --> the amount of money that the transaction will transfer
    @dimension(int)
    def txn_amount(self): return self.__txn_amount
    @txn_amount.setter
    def txn_amount(self, v): self.__txn_amount = v

    # txn_type --> "W" = Withdraw, "D" = Deposit, "T" = Transfer
    @dimension(int)
    def txn_type(self): return self.__txn_type
    @txn_type.setter
    def txn_type(self, v): self.__txn_type = v

    # processed --> bool indicating if the txn has been completed
    @dimension(bool)
    def processed(self): return self.__processed
    @processed.setter
    def processed(self, v): self.__processed = v

    # from_c --> instance of this Customer's attributes when -MAKING- the transaction (is changed outside of this Transaction)
    @dimension(Customer)
    def from_c(self): return self.__from_c
    @from_c.setter
    def from_c(self, v): self.__from_c = v

    # to_c --> instance of this Customer's attributes when -RECIEVING- the transaction (is changed outside of this Transaction)
    @dimension(Customer)
    def to_c(self): return self.__to_c
    @to_c.setter
    def to_c(self, v): self.__to_c = v

    def __init__(self, from_c, to_c):
        self.txn_id = str(uuid.uuid4())  # Have to do this manuelly because spacetime was not giving it a @primarykey
        self.txn_amount = from_c.txn_amount
        self.txn_type = from_c.txn_type
        self.processed = False
        self.from_c = from_c.account_number
        self.to_c = None
        if to_c:
            self.to_c = to_c.account_number

        # old way #
        #self.from_c = from_c
        #self.to_c = to_c

    def complete_process(self): self.processed = True

    def __str__(self):
        return "[TXN NO : {:s}] - [AMO : {:7d}] - [TXN TYPE : {:s}] - [PROC : {:s}] - [FROM_C AN : {:s}] - [TO_C AN : {:s}]".format(
            str(self.txn_id), self.txn_amount, str(self.txn_type), str(self.processed), str(self.from_c), str(self.to_c))


@subset(Transaction)
class NewValidTransaction(Transaction):
    @staticmethod
    def __predicate__(transaction):
        return transaction.txn_amount < 1000000 and not transaction.processed


@subset(Transaction)
class NewRedAlertTransaction(Transaction):
    @staticmethod
    def __predicate__(transaction):
        return transaction.txn_amount > 1000000 and not transaction.processed


@pcc_set
class BankingRecord(object):
    """
    classdocs
    """

    # ID --> spacetime key for BankingRecord object (is the same as the customer
    #        that made the transaction
    @primarykey(str)
    def ID(self): return self._ID
    @ID.setter
    def ID(self, value): self._ID = value

    # record --> list of dicts that contain transaction history of the customer 
    @dimension(list)
    def record(self): return self.__record
    @record.setter
    def record(self, value): self.__record = value

    def update_record(self, txn):
        if txn.txn_type == "W" or txn.txn_type == "D":
            self.record = self.record + [{"TXN TYPE": txn.txn_type, "TXN AMOUNT": txn.txn_amount, "FROM_C": txn.from_c}]
        elif txn.txn_type == "T":
           self.record = self.record + [{"TXN TYPE": txn.txn_type, "TXN AMOUNT": txn.txn_amount, "FROM_C": txn.from_c, "TO_C": txn.to_c}]

    def return_formated_records(self):
        """ Method that returns the dicts in .record easily formatted """
        return str(self.record)

    def __init__(self, txn):
        self.ID = txn.from_c
        self.record = []
        self.update_record(txn)


if __name__ == "__main__":
    pass
