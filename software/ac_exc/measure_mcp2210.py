#!/usr/bin/python3

#uncomment for debbug purposes
#import logging
#logging.basicConfig(level=logging.DEBUG) 

import sys
import time
import datetime
from mcp2210 import Mcp2210, Mcp2210GpioDesignation, Mcp2210GpioDirection


#from pymlab import config
import logging

from BRIDGEADC01 import BRIDGEADC01

"""
Show data from BRIDGEADC01 module over MCP2210. 
"""

class SPIWraper:
    def __init__(self,cs_pins):
        self.mcp=Mcp2210(serial_number="0001112676")
        self.mcp.configure_spi_timing(chip_select_to_data_delay=0,
                                 last_data_byte_to_cs=0,
                                 delay_between_bytes=0)

        self.mcp._get_spi_configuration()
        self.mcp._spi_settings.bit_rate=400000
        self.mcp._spi_settings.mode=3
        self.mcp._set_spi_configuration()

        for i in range(len(cs_pins)):
            self.mcp.set_gpio_designation(cs_pins[i], Mcp2210GpioDesignation.CHIP_SELECT)

        self.result=[];

    def SPI_write(self,cs,data):
        '''write data to bus with selected CS pin'''
        tmpresult=self.mcp.spi_exchange(bytes(data), cs)
        self.result=[x for x in tmpresult]

    def SPI_read(self,num_bytes):
        '''read result from last transaction'''
        return self.result;



import numpy as np
LOGGER = logging.getLogger(__name__)

spi = SPIWraper([4])

try:
    #print("SPI configuration..")
    #spi.SPI_config(spi.I2CSPI_MSB_FIRST| spi.I2CSPI_MODE_CLK_IDLE_LOW_DATA_EDGE_LEADING| spi.I2CSPI_CLK_461kHz)
    #spi.GPIO_config(spi.I2CSPI_SS2 | spi.I2CSPI_SS3, spi.SS2_INPUT | spi.SS3_INPUT)

    print("Weight scale configuration..")
    scale = BRIDGEADC01(spi,4,1)
    scale.reset()

    freq=scale.setFilterAC(200)
    sys.stdout.write("frekvence vyčítání: %4.2f;\n" %(freq))
    sys.stdout.flush()

    f = open("calibration.txt","r")
    lines = f.readlines()
    f.close()    

    i=0
    for line in lines:
        if i>1:
            break
        vals=line.split()
        scale.setChannelOnly(i)
        scale.setOffsetRegister(int(vals[0]))
        scale.setFullScaleRegister(int(vals[1]))
        scale.setUnitCalibrationGain(float(vals[2]))
        i += 1
 
    sys.stdout.write("datetime; freq; channel1;\n")
    sys.stdout.flush()
    scale.startConntinuousConversion(0)
    lastTime=time.time();
    while 1:
        if scale.isBusy():
            sys.stdout.write("busy")
            sys.stdout.flush()
            time.sleep(0.25)
            continue
        currentTime=time.time();
        ts = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
        channel1 = scale.measureWeight()
        sys.stdout.write("%s; %4.1f; %+4.3f;\n" %(ts, 1/(currentTime-lastTime), channel1))
        sys.stdout.flush()
        lastTime=currentTime
        
except KeyboardInterrupt:
    sys.exit(0)









