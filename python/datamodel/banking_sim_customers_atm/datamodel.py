"""
Created on June 28, 2017

@author: RobertXavierMaldonado
"""


#############################################################################################


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


#############################################################################################


@pcc_set
class Customer(object):
    """Class for modelling a customer from a Bank's point of view"""

    @primarykey(str)
    def account_number(self): return self.__account_number
    @account_number.setter
    def account_number(self, v): self.__account_number = v

    @dimension(str)
    def txn_type(self): return self.__txn_type
    @txn_type.setter
    def txn_type(self, v): self.__txn_type = v

    @dimension(str)
    def name(self): return self.__name
    @name.setter
    def name(self, v): self.__name = v

    @dimension(int)
    def balance(self): return self.__balance
    @balance.setter
    def balance(self, v): self.__balance = v

    def give_account_number(self): return self.__account_number

    def give_name(self): return self.__name

    def give_balance(self): return self.__balance

    def give_txn_type(self): return self.__txn_type

    def __init__(self):
        self.txn_type = choice(["W", "D"])
        self.name = randrange(1, 999)
        self.balance = randrange(1, 1050000)

    def __str__(self):
        return "[ACC_NO : {:s}] - [NAME : {:3d}] - [TYPE : {:s}] - [BAL : {:7d}]".format(str(self.give_account_number()), self.give_name(), str(self.give_txn_type()), self.give_balance())

#############################################################################################


@projection(Customer, Customer.account_number, Customer.name)
class CustomerView(Customer):
    """Class for modelling the what the customeer is allowed to view"""

    def __str__(self):
        return "[ACC_NO : {:s}] - [NAME : {:3d}]".format(str(self.give_account_number()), self.give_name())


#############################################################################################

@pcc_set
class Transaction(object):
    """A trasaction made by the customer"""

    @primarykey(str)
    def txn_id(self): return self.__txn_id
    @txn_id.setter
    def txn_id(self, v): self.__txn_id = v

    @dimension(str)
    def customer_an(self): return self.__customer_an
    @customer_an.setter
    def customer_an(self, v): self.__customer_an = v

    @dimension(float)
    def amount(self): return self.__amount
    @amount.setter
    def amount(self, v): self.__amount = v

    @dimension(str)
    def type(self): return self.__type
    @type.setter
    def type(self, v): self.__type = v

    @dimension(bool)
    def processed(self): return self.__processed
    @processed.setter
    def processed(self, v): self.__processed = v


    # @dimension(Customer)
    # def from_ac(self): return self.__from_ac
    # @from_ac.setter
    # def from_ac(self, v): self.__from_ac = v
    #
    # @dimension(Customer)
    # def to_ac(self): return self.__to_ac
    # @to_ac.setter
    # def to_ac(self, v): self.__to_ac = v

    def give_txn_id(self): return self.__txn_id

    def give_customer_an(self): return self.__customer_an

    def give_amount(self): return self.__amount

    def give_type(self): return self.__type

    def give_processed(self): return self.__processed

    def complete_process(self): self.__processed = True

    # def give_from_ac(self): return self.__from_ac
    #
    # def give_to_ac(self): return self.__to_ac

    def __init__(self, customer):
        self.txn_id = str(uuid.uuid4())  # Have to do this manuelly because spacetime was not giving it a @primarykey
        self.amount = customer.give_balance()
        self.type = customer.give_txn_type()
        self.customer_an = customer.give_account_number()
        self.processed = False

        # self.from_ac = customer
        # self.to_ac = customer

    def __str__(self):
        return "[TXN NO : {:s}] - [CUSTOMER AN : {:s}] - [AMO : {:7d}] - [TYPE : {:s}] - [PROC : {:s}]".format(self.give_txn_id(), self.give_customer_an(), self.give_amount(), self.give_type(), str(self.give_processed()))


@subset(Transaction)
class NewValidTransaction(Transaction):
    @staticmethod
    def __predicate__(transaction):
        return transaction.give_amount() < 1000000 and not transaction.give_processed()


@subset(Transaction)
class NewRedAlertTransaction(Transaction):
    @staticmethod
    def __predicate__(transaction):
        return transaction.give_amount() > 1000000 and not transaction.give_processed()


#############################################################################################


@pcc_set
class BankingRecord(object):
    """
    classdocs
    """

    ###############################

    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    _Record = []
    @dimension(list)
    def Record(self):
        return self._Record

    @Record.setter
    def Record(self, value):
        self._Record = value

    ##############################

    def give_Record(self):
        return self.Record

    def return_formated_records(self):
        master_str = ""
        for r in self.Record:
            master_str += " --- " + str(r)
        return master_str

    # def __contains__(self, item):
    #     pass

    def __init__(self, txn):
        self.ID = txn.give_customer_an()
        self.Record = []


#############################################################################################


if __name__ == "__main__":
    pass

'''

from __future__ import absolute_import
from random import randrange, choice
import logging
from pcc.join import join
from pcc.subset import subset
from pcc.parameter import parameter, ParameterMode
from pcc.projection import projection
from pcc.set import pcc_set
from pcc.attributes import dimension, primarykey

import traceback

logger = logging.getLogger(__name__)
LOG_HEADER = "[DATAMODEL]"

#############################################################################################


@pcc_set
class Customer(object):
    """
    classdocs
    """

    ###############################
    # _ID = None
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    # _Transaction = None
    @dimension(str)
    def Transaction(self):
        return self._Transaction

    @Transaction.setter
    def Transaction(self, value):
        self._Transaction = value

    # _Amount = 0
    @dimension(int)
    def Amount(self):
        return self._Amount

    @Amount.setter
    def Amount(self, value):
        self._Amount = value

    # _RedAlert = None
    @dimension(bool)
    def RedAlert(self):
        return self._RedAlert

    @RedAlert.setter
    def RedAlert(self, value):
        self._RedAlert = value

    # _Completed = None
    @dimension(bool)
    def Completed(self):
        return self._Completed

    @Completed.setter
    def Completed(self, value):
        self._Completed = value

    # _Storage = 0
    @dimension(int)
    def Storage(self):
        return self._Storage

    @Storage.setter
    def Storage(self, value):
        self._Storage = value

    ###############################

    def give_ID(self):
        return self.ID

    def give_Transaction(self):
        return self.Transaction

    def give_Amount(self):
        return self.Amount

    def give_Completed(self):
        return self.Completed

    def give_Storage(self):
        return self.Storage

    def give_RedAlert(self):
        return self.RedAlert

    def raise_RedAlert(self):
        self.RedAlert = False

    def confirm_completion(self):
        self.Completed = True

    def randomize_Transaction(self):
        self.Completed = False
        self.Transaction = choice(["W", "D"])
        self.Amount = randrange(1, 1010000)
        self.Storage = 0
        if self.give_Transaction() == "D":
            self.Storage = self.give_Amount()
        # print("Type --> ", self.Transaction, "Ammount --> ", self.Amount, "Storage --> ", self.Storage)

    ###############################

    def __str__(self):
        return "[Type : {:s}] - [Amou : {:7d}] - [Stor : {:7d}] - [Compl : {}] - [RedA : {}] - [ID : {}]".format(str(self.give_Transaction()), self.give_Amount(), self.give_Storage(), str(self.Completed), str(self.give_RedAlert()), self.give_ID() )

    def __init__(self):
        self.RedAlert = False
        self.randomize_Transaction()


@subset(Customer)
class ValidCustomer(Customer):
    """
    classdocs
    """
    # @staticmethod
    # def __query__(customers):
    #     return [c for c in customers if DepositingCustomer.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return not c.give_RedAlert()

    def transfer_am_to_stor(self):
        if self.give_Transaction() == "W":
            self.Storage += self.Amount
        elif self.give_Transaction() == "D":
            self.Storage -= self.Amount
            if self.Storage < 0:
                self.Storage = 0


@subset(Customer)
class InvalidCustomer(Customer):
    """
    classdocs
    """
    # @staticmethod
    # def __query__(customers):
    #     return [c for c in customers if WithdrawingCustomer.__predicate__(c)]

    @staticmethod
    def __predicate__(c):
        return c.give_RedAlert


#############################################################################################


@pcc_set
class BankingRecord(object):
    """
    classdocs
    """

    ###############################

    _ID = None
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    _Record = []
    @dimension(list)
    def Record(self):
        return self._Record

    @Record.setter
    def Record(self, value):
        self._Record = value

    ##############################

    def give_Record(self):
        return self.Record

    def add_to(self, value):
        self.Record.append(value)

    def __str__(self):
        return "[ID : {:s}] - [True : {:4d}] - [False : {:4d}]".format(self.ID, self.Record.count(True), self.Record.count(False))


    # def __contains__(self, item):
    #     pass

    def __init__(self, customer):
        self.ID = customer.give_ID()
        self.Record = []


#############################################################################################


@pcc_set
class ATM(object):

    ###############################

    # _ID = None
    @primarykey(str)
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    # _Storage = 0
    @dimension(int)
    def Storage(self):
        return self._Storage

    @Storage.setter
    def Storage(self, value):
        self._Storage = value

    ###############################
    def give_Storage(self):
        return self.Storage

    def transfer_am_to_stor(self, customer):
        if type(customer) == ValidCustomer:
            amount = customer.give_Amount()
            if customer.give_Transaction() == "W":
                amount = -amount
            self.Storage += amount

    def check_Transaction(self, customer):
        if customer.give_Amount() > 1000000:
            return False
        return True

    def execute_Transaction(self, customer):

        # Confirm that the transaction has happened
        customer.confirm_completion()

        # Transfer funds between customer and atm
        self.transfer_am_to_stor(customer)
        customer.transfer_am_to_stor()

        return self.check_Transaction(customer)

    ###############################

    def __str__(self):
        return "[1] ATM Stor -> " + str(self.give_Storage())

    def __init__(self):
        self.Storage = 0


#############################################################################################

'''







































































