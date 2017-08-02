#!/usr/bin/python
'''
Created on June 29, 2017

@author: Robert Xavier Maldonado
'''

import logging
import logging.handlers
import os
import sys

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "../..")))

from spacetime.client.frame import frame
from applications.banking.bankingsim_customer import CustomerSimulation
from applications.banking.bankingsim_atm import ATMSimulation
from applications.banking.bankingsim_watchdog import WatchDogSimulation

logger = None

class Simulation(object):
    """
    classdocs
    """
    def __init__(self):
        """
        constructor
        """
        wait_time = 4000  # Used in every simulation

        frame_customer_0 = frame(time_step=wait_time)
        customer_app_0 = CustomerSimulation(frame_customer_0)
        frame_customer_0.attach_app(customer_app_0)

        frame_customer_1 = frame(time_step=wait_time)
        customer_app_1 = CustomerSimulation(frame_customer_1)
        frame_customer_1.attach_app(customer_app_1)

        frame_customer_2 = frame(time_step=wait_time)
        customer_app_2 = CustomerSimulation(frame_customer_2)
        frame_customer_2.attach_app(customer_app_2)

        frame_customer_3 = frame(time_step=wait_time)
        customer_app_3 = CustomerSimulation(frame_customer_3)
        frame_customer_3.attach_app(customer_app_3)

        frame_customer_4 = frame(time_step=wait_time)
        customer_app_4 = CustomerSimulation(frame_customer_4)
        frame_customer_4.attach_app(customer_app_4)

        frame_customer_5 = frame(time_step=wait_time)
        customer_app_5 = CustomerSimulation(frame_customer_5)
        frame_customer_5.attach_app(customer_app_5)

        frame_customer_6 = frame(time_step=wait_time)
        customer_app_6 = CustomerSimulation(frame_customer_6)
        frame_customer_6.attach_app(customer_app_6)

        frame_customer_7 = frame(time_step=wait_time)
        customer_app_7 = CustomerSimulation(frame_customer_7)
        frame_customer_7.attach_app(customer_app_7)

        frame_customer_8 = frame(time_step=wait_time)
        customer_app_8 = CustomerSimulation(frame_customer_8)
        frame_customer_8.attach_app(customer_app_8)

        frame_customer_9 = frame(time_step=wait_time)
        customer_app_9 = CustomerSimulation(frame_customer_9)
        frame_customer_9.attach_app(customer_app_9)

########################################################################################################################

        frame_atm = frame(time_step=(wait_time/10))
        atm_app = ATMSimulation(frame_atm)
        frame_atm.attach_app(atm_app)

########################################################################################################################

        frame_watchdog = frame(time_step=(wait_time/10))
        watchdog_app = WatchDogSimulation(frame_watchdog)
        frame_watchdog.attach_app(watchdog_app)

########################################################################################################################

        frame_customer_0.run_async()
        frame_customer_1.run_async()
        frame_customer_2.run_async()
        frame_customer_3.run_async()
        frame_customer_4.run_async()
        frame_customer_5.run_async()
        frame_customer_6.run_async()
        frame_customer_7.run_async()
        frame_customer_8.run_async()
        frame_customer_9.run_async()

        frame_atm.run_async()

        frame_watchdog.run_async()

        frame.loop()

def SetupLoggers():
    # Not quite sure what this does
    global logger
    logger = logging.getLogger()
    logging.info("testing before")
    logger.setLevel(logging.DEBUG)

    # logfile = os.path.join(os.path.dirname(__file__), "../../logs/CADIS.log")
    # flog = logging.handlers.RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=50, mode='w')
    # flog.setFormatter(logging.Formatter('%(levelname)s [%(name)s] %(message)s'))
    # logger.addHandler(flog)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    clog = logging.StreamHandler()
    clog.addFilter(logging.Filter(name='CADIS'))
    clog.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    clog.setLevel(logging.DEBUG)
    logger.addHandler(clog)

if __name__ == "__main__":
    SetupLoggers()
    sim = Simulation()
