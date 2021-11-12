#!/usr/bin/env python
__author__ = "@KaosNeverDied forgettable.eth"
__copyright__ = "whatever"
__credits__ = ["@kaosNeverdied"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "@KaosNeverdied"
__status__ = "Prototype"

import logging
import time

from seasnake import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG) #NOTE: minimum logging level - set this to whatever suits your needs

#config logging
stream_handler = logging.StreamHandler() 
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO) 
file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG) 
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':

    #NOTE: Basic example of use
    asset_contract_address = "0x06012c8cf97bead5deae237070f9587f8e7a266d"
    token_id = "1"
    opensea = OpenSea()
    asset = opensea.get_asset_single(asset_contract_address=asset_contract_address, token_id=token_id)
    print(f'id: {asset.id}')
    print(f'token_id: {asset.token_id}')
    print(f'background_color: {asset.background_color}')
    print(f'img_url: {asset.image_url}')
