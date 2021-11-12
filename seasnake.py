import itertools
import logging
import requests
import logging
import typing
#import collections.abc
import pandas as pd
from itertools import combinations
import json
from datetime import datetime

#NOTE: If you don't have logger set up in your root .py file the logging statments will cause errors. 
#comment out all logger statement or add logging to your root file
logger = logging.getLogger()


class Asset:
    def __init__(self, data: dict):   
        logger.info(f'New Asset object created with keys {data.keys()}')
        self.id = data['id'] 
        self.token_id = data['token_id'] 
        self.num_sales = data['num_sales'] 
        self.background_color = data['background_color']
        self.image_url = data['image_url'] 
        self.image_preview_url = data['image_preview_url'] 
        self.image_thumbnail_url = data['image_thumbnail_url'] 
        self.image_original_url = data['image_original_url']
        self.animation_url = data['animation_url']
        self.animation_original_url = data['animation_original_url'] 
        self.name = data['name'] 
        self.description = data['description'] 
        self.external_link = data['external_link'] 
        self.asset_contract = Contract(data['asset_contract'])
        self.permalink = data['permalink']
        self.collection = Collection(data['collection'])
        self.decimals = data['decimals']
        self.token_metadata = data['token_metadata'] 
        self.owner = Owner(data['owner']) 
        
        
        if 'sell_orders' in data.keys(): 
            self.sell_orders = data['sell_orders'] 
        if 'creator' in data.keys():
            self.creator = Creator(data['creator']) 
        if 'traits' in data.keys():
            self.traits: typing.List[Traits] = [Traits(trait) for trait in data['traits']]
            self.traits_qty = len(data['traits'])
        if 'last_sale' in data.keys():
            self.last_sale = data['last_sale'] 
        if 'top_bid' in data.keys():
            self.top_bid = data['top_bid'] 
        if 'listing_date' in data.keys():
            self.listing_date = data['listing_date'] 
        if 'is_presale' in data.keys():
            self.is_presale = data['is_presale'] 
        if 'transfer_fee_payment_token' in data.keys():
            self.transfer_fee_payment_token = data['transfer_fee_payment_token'] 

    

class Stakeholder:
    def __init__(self, data) -> None:
        self.user = data['user'] #TODO: Dict of form: {"username": "NullAddress"} - class?
        self.profile_img_url = data['profile_img_url'] 
        self.address = data['address'] 
        self.config = data['config']

class Owner(Stakeholder):
    def __init__(self, data) -> None:
        logger.info(f'New Owner object created with keys {data.keys()}')
        super().__init__(data)

class Creator(Stakeholder):
    def __init__(self, data) -> None:
        logger.info(f'New Creator object created with keys {data.keys()}')
        super().__init__(data)

class Seller(Stakeholder):
    def __init__(self, data) -> None:
        logger.info(f'New Seller object created with keys {data.keys()}')
        super().__init__(data)

class FromAccount(Stakeholder):
    def __init__(self, data) -> None:
        logger.info(f'New stakeholer object created with keys {data.keys()}')
        super().__init__(data)


#TODO: Traits keys seem to vary, so this class might need to be removed and Traits remain a dictionary object 
class Traits:
    def __init__(self, data):
        logger.info(f'New Traits object created with keys {data.keys()}')
        self.trait_type = data['trait_type']
        self.value = data['value'] 
        self.display_type = data['display_type'] 
        self.max_value = data['max_value'] 
        self.trait_count = data['trait_count'] 
        self.order = data['order']
        
    
class Event:
    def __init__(self, data) -> None:
        logger.info(f'New Event object created with keys {data.keys()}')
        self.approved_account = data['approved_account']
        self.asset = Asset(data['asset'])
        self.asset_bundle = data['asset_bundle']
        self.auction_type = data['auction_type']
        self.bid_amount = data['bid_amount']
        self.collection_slug = data['collection_slug']
        self.contract_address = data['contract_address']
        self.created_date = data['created_date']
        self.custom_event_name = data['custom_event_name']
        self.dev_fee_payment_event = data['dev_fee_payment_event']
        self.duration = data['duration']
        self.ending_price = data['ending_price']
        self.event_type = data['event_type']
        self.from_account = FromAccount(data['from_account']) if data['from_account'] is not None else None 
        self.id = data['id']
        self.is_private = data['is_private']
        self.owner_account = data['owner_account']
        self.payment_token = PaymentToken(data['payment_token'])  if data['payment_token'] is not None else None 
        self.quantity = data['quantity']
        self.seller = Seller(data['seller']) if data['seller'] is not None else None
        self.starting_price = data['starting_price']
        self.to_account = data['to_account']
        self.total_price = data['total_price']
        self.transaction = data['transaction']
        self.winner_account = data['winner_account']


class PaymentToken:
    def __init__(self, data) -> None:
        logger.info(f'New PaymentToken object created with keys {data.keys()}')
        self.id = data['id']
        self.symbol = data['symbol']
        self.address = data['address']
        self.image_url = data['image_url']
        self.name = data['name']
        self.decimals = data['decimals']
        self.eth_price = data['eth_price']
        self.usd_price = data['usd_price']
        

class Collection:
    def __init__(self, data) -> None:
        logger.info(f'New Collection object created with keys {data.keys()}')
 
        if 'primary_asset_contracts' in data.keys():
            self.primary_asset_contracts = data['primary_asset_contracts']         
        if 'traits' in data.keys():
            self.traits = data['traits'] 
        if 'stats' in data.keys():
            self.stats = CollectionStats(data['stats'])
        
        self.banner_image_url = data['banner_image_url'] 
        self.chat_url = data['chat_url']
        self.created_date = data['created_date']
        self.default_to_fiat = data['default_to_fiat']
        self.description = data['description']
        self.dev_buyer_fee_basis_points = data['dev_buyer_fee_basis_points'] 
        self.dev_seller_fee_basis_points = data['dev_seller_fee_basis_points']
        self.discord_url = data['discord_url']
        self.display_data = data['display_data']  
        self.external_url = data['external_url']
        self.featured = data['featured'] 
        self.featured_image_url = data['featured_image_url']   
        self.hidden = data['hidden'] 
        self.safelist_request_status = data['safelist_request_status']  
        self.image_url = data['image_url'] 
        self.is_subject_to_whitelist = data['is_subject_to_whitelist']
        self.large_image_url = data['large_image_url']
        self.medium_username = data['medium_username']
        self.name = data['name'] 
        self.only_proxied_transfers = data['only_proxied_transfers']
        self.opensea_buyer_fee_basis_points = data['opensea_buyer_fee_basis_points']
        self.opensea_seller_fee_basis_points = data['opensea_seller_fee_basis_points']
        self.payout_address = data['payout_address']
        self.require_email = data['require_email']
        self.short_description = data['short_description']
        self.slug = data['slug']
        self.telegram_url = data['telegram_url']
        self.twitter_username = data['twitter_username']
        self.instagram_username = data['instagram_username']
        self.wiki_url = data['wiki_url']
        
class CollectionStats:
    def __init__(self, data) -> None:
        logger.info(f'New CollectionStats object created with keys {data.keys()}')
        self.one_day_volume = data['one_day_volume']
        self.one_day_change = data['one_day_change']
        self.one_day_sales = data['one_day_sales']
        self.one_day_average_price = data['one_day_average_price']
        self.seven_day_volume = data['seven_day_volume']
        self.seven_day_change = data['seven_day_change']
        self.seven_day_sales = data['seven_day_sales']
        self.seven_day_average_price = data['seven_day_average_price']
        self.thirty_day_volume = data['thirty_day_volume']
        self.thirty_day_change = data['thirty_day_change']
        self.thirty_day_sales = data['thirty_day_sales']
        self.thirty_day_average_price = data['thirty_day_average_price']
        self.total_volume = data['total_volume']
        self.total_sales = data['total_sales']
        self.total_supply = data['total_supply']
        self.count = data['count']
        self.num_owners = data['num_owners']
        self.average_price = data['average_price']
        self.num_reports = data['num_reports']
        self.market_cap = data['market_cap']
        self.floor_price = data['floor_price']
        


class Bundle:
    def __init__(self, data) -> None:
        self.maker = data['maker'] 
        self.slug = data['slug'] 
        self.assets = [Asset(asset) for asset in data['assets']] 
        self.name = data['name']
        self.description = data['description']
        self.external_link = data['external_link']
        self.asset_contract = data['asset_contract']
        self.permalink = data['permalink']
        self.sell_orders = data['sell_orders'] 

class Contract:
    def __init__(self, data) -> None:
        logger.info('New Contract Object created')
        self.address = data['address']
        self.asset_contract_type = data['asset_contract_type']
        self.created_date = data['created_date']
        self.name = data['name']
        self.nft_version = data['nft_version']
        self.opensea_version = data['opensea_version']
        self.owner = data['owner']
        self.schema_name = data['schema_name']
        self.symbol = data['symbol']
        self.total_supply = data['total_supply']
        self.description = data['description']
        self.external_link = data['external_link']
        self.image_url = data['image_url']
        self.default_to_fiat = data['default_to_fiat']
        self.dev_buyer_fee_basis_points = data['dev_buyer_fee_basis_points']
        self.dev_seller_fee_basis_points = data['dev_seller_fee_basis_points']
        self.only_proxied_transfers = data['only_proxied_transfers']
        self.opensea_buyer_fee_basis_points = data['opensea_buyer_fee_basis_points']
        self.opensea_seller_fee_basis_points = data['opensea_seller_fee_basis_points']
        self.buyer_fee_basis_points = data['buyer_fee_basis_points']
        self.seller_fee_basis_points = data['seller_fee_basis_points']
        self.payout_address = data['payout_address']


class OpenSea:
    def __init__(self) -> None:
        self._baseurl_assets = "https://api.opensea.io/api/v1/assets?"
        self._baseurl_asset_contract = "https://api.opensea.io/api/v1/assets_contract"
        self._baseurl_asset_contract_single = "https://api.opensea.io/api/v1/asset_contract"
        self._baseurl_events = "https://api.opensea.io/api/v1/events?"
        self._baseurl_collections = "https://api.opensea.io/api/v1/collections?"
        self._baseurl_bundles = "https://api.opensea.io/api/v1/bundles?"
    

    def _make_request(self, url: str, file_name : typing.Union[str, None]):
        '''
        Receives a url and returns a .json object 
        '''
        try:
            print(f'URL: {url}')
            headers = {"Accept": "application/json"}
            get_json = requests.get(url)
            results = get_json.json()
        except TypeError as e:
            logger.error(f'connectionmanager.get_asset(): TypeError {e}')
        except exception as e:
            logger.error(f'connectionmanager.get_asset(): {e}')
        else:
            #print(results)
            #self._write_json(file_name, results)
            return results
    

           
    
    #REF: https://docs.opensea.io/reference/getting-assets
    def get_assets(self, owner: typing.Union[str, None] = None, token_ids: typing.Union[str, None] = None, 
    asset_contract_address: typing.Union[str, None] = None, asset_contract_addresses: typing.Union[typing.List, None] = None, 
    order_by: typing.Union[str, None] = None, order_direction: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, 
    limit: typing.Union[str, None] = None, collection: typing.Union[str, None] = None) -> typing.List[Asset]:
        '''
        Pass in any required parameters for an assets search. Returns a list of Asset objects 
        '''
        
        req_str = []        
        if owner is not None: 
            req_str.append(f"owner={owner}")
        if token_ids is not None:
            req_str.append(f"&token_ids={token_ids}") if len(req_str) >=0 else req_str.append(f"token_ids={token_ids}")
        if asset_contract_address is not None:
            req_str.append(f"&asset_contract_address={asset_contract_address}") if len(req_str) >=0 else req_str.append(f"asset_contract_address={asset_contract_address}")
        if asset_contract_addresses is not None:
            req_str.append(f"&asset_contract_addresses={asset_contract_addresses}") if len(req_str) >=0 else req_str.append(f"asset_contract_addresses={asset_contract_addresses}")
        if order_by is not None:
            req_str.append(f"&order_by={order_by}") if len(req_str) >=0 else req_str.append(f"order_by={order_by}")
        if order_direction is not None:
            req_str.append(f"&order_direction={order_direction}") if len(req_str) >=0 else req_str.append(f"order_direction={order_direction}")
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >=0 else req_str.append(f"offset={offset}")
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >=0 else req_str.append(f"limit={limit}")
        if collection is not None:
            req_str.append(f"&collection={collection}") if len(req_str) >=0 else req_str.append(f"collection={collection}")
        
        url_request_string = self._baseurl_assets + ''.join(req_str)
        results = self._make_request(url_request_string, 'get_assets')
        
        assets = []
        for asset in results['assets']:
            assets.append(Asset(asset))
        
        return assets
    


    #FIXME: Need error handling etc
    #REF: https://docs.opensea.io/reference/retrieving-asset-events
    def get_events(self, asset_contract_address: typing.Union[str, None] = None, collection_slug: typing.Union[str, None] = None, 
    token_id : typing.Union[str, None] = None, account_address : typing.Union[str, None] = None, event_type: typing.Union[str, None] = None, 
    only_opensea: typing.Union[str, None] = None, auction_type: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, 
    limit: typing.Union[str, None] = None, occurred_before: typing.Union[str, None] = None, occurred_after: typing.Union[str, None] = None) -> typing.List[Event]:
        '''
        Pass in any required parameters for an events  search. Returns a list of event Objects 
        '''

        req_str = []

        if asset_contract_address is not None:
            req_str.append(f"asset_contract_address={asset_contract_address}") 
        if collection_slug is not None:
            req_str.append(f"&collection_slug={collection_slug}") if len(req_str) >= 0 else req_str.append(f"collection_slug={collection_slug}")  
        if token_id is not None:
            req_str.append(f"&token_id={token_id}") if len(req_str) >= 0 else req_str.append(f"token_id={token_id}")  
        if account_address is not None:
            req_str.append(f"&account_address={account_address}") if len(req_str) >= 0 else req_str.append(f"account_address={account_address}")  
        if event_type is not None:
            req_str.append(f"&event_type={event_type}") if len(req_str) >= 0 else req_str.append(f"event_type={event_type}")  
        if only_opensea is not None:
            req_str.append(f"&only_opensea={only_opensea}") if len(req_str) >= 0 else req_str.append(f"only_opensea={only_opensea}")  
        if auction_type is not None:
            req_str.append(f"&auction_type={auction_type}") if len(req_str) >= 0 else req_str.append(f"auction_type={auction_type}")  
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"offset={offset}")  
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"limit={limit}")             
        if occurred_before is not None:
            req_str.append(f"&occurred_before={occurred_before}") if len(req_str) >= 0 else req_str.append(f"occurred_before={occurred_before}")             
        if occurred_after is not None:
            req_str.append(f"&occurred_after={occurred_after}") if len(req_str) >= 0 else req_str.append(f"occurred_after={occurred_after}")

        url_request_string = self._baseurl_events + ''.join(req_str) 
        results = self._make_request(url_request_string, 'get_events')
        events = []

        for event in results['asset_events']:
            events.append(Event(event))
        return events
                    
 
    #REF: https://docs.opensea.io/reference/retrieving-collections 
    def get_collections(self, asset_owner: typing.Union[str, None] = None, offset: typing.Union[str, None] = None, limit: typing.Union[str, None] = None) -> typing.List[Collection]:
        '''
        Pass in any required parameters for a collections search. Returns a list of Collection objects 
        '''
        
        req_str = []
        if asset_owner is not None:
            req_str.append(f"asset_owner={asset_owner}")
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"&offset={offset}")
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"&limit={limit}")

        url_request_string = self._baseurl_collections + ''.join(req_str) 
        results = self._make_request(url_request_string, 'get-collections')
        collections = []
        for collection in results['collections']:
            collections.append(Collection(collection))
        return collections            
        

    #RE: https://docs.opensea.io/reference/retrieving-bundles
    def get_bundles(self, on_sale: typing.Union[str, None] = None, owner: typing.Union[str, None] = None, asset_contract_address: typing.Union[str, None] = None, 
    token_ids: typing.Union[str, None] = None, limit: typing.Union[str, None] = None, offset: typing.Union[str, None] = None) -> typing.List[Bundle]:
        '''
        Pass in any required parameters for a bundles search. Returns a list of Bundle objects 
        '''
        
        req_str = []
        if on_sale is not None:
            req_str.append(f"on_sale={on_sale}")
        if owner is not None:
            req_str.append(f"&owner={owner}") if len(req_str) >= 0 else req_str.append(f"owner={owner}") 
        if asset_contract_address is not None:
            req_str.append(f"&asset_contract_address={asset_contract_address}") if len(req_str) >= 0 else req_str.append(f"asset_contract_address={asset_contract_address}") 
        if token_ids is not None:
            req_str.append(f"&token_ids={token_ids}") if len(req_str) >= 0 else req_str.append(f"token_ids={token_ids}") 
        if limit is not None:
            req_str.append(f"&limit={limit}") if len(req_str) >= 0 else req_str.append(f"limit={limit}") 
        if offset is not None:
            req_str.append(f"&offset={offset}") if len(req_str) >= 0 else req_str.append(f"offset={offset}") 

        url_request_string = self._baseurl_bundles + ''.join(req_str) 
        results = self._make_request(url_request_string, 'get_bundles')
        bundles = []

        for bundle in bundles:
            bundles.append(Bundle(bundle))
        return bundles


    # REF: https://docs.opensea.io/reference/retrieving-a-single-asset
    def get_asset_single(self, asset_contract_address: typing.Union[str, None] = None, token_id: typing.Union[str, None] = None, account_address: typing.Union[str, None] = None) -> Asset:
        '''
        Pass in any required parameters for an asset search. Returns a single Asset object 
        '''

        if asset_contract_address is not None and token_id is not None:
            req_str = []
            req_str.append(f'/{asset_contract_address}/{token_id}/')
            
            if account_address is not None:
                req_str.append(f"?account_address={account_address}")
            
            url_request_string = self._baseurl_assets[0:(len(self._baseurl_assets)-2)] + ''.join(req_str)
            print(f'STRING: {url_request_string}') 
            result = self._make_request(url_request_string, 'get_asset_single')
            return Asset(result)
        else:
            #TODO: Pop and alert informing the user that the string is empty
            logger.warning("Opensea.get_asset_single(): user did not pass asset_contract_address and token_id which are required strings")
            

    # REF: https://docs.opensea.io/reference/retrieving-a-single-contract 
    def get_contract_single(self, asset_contract_address: str) -> Contract:
        '''
        Pass in the asset_contract_address for a given contract. Returns a contract object 
        '''
        url_request_string = self._baseurl_asset_contract_single + f"/{asset_contract_address}" 
        result = self._make_request(url_request_string, 'get_contract_single')    
        #FIXME: Check contract is actually got something, otherwise just return an empty dict?            
        return Contract(result) 

    # REF: https://docs.opensea.io/reference/retrieving-a-single-collection
    def get_collection_single(self, collection_slug) -> Collection:
        '''
        Pass in the collection_slug for a single collection. Returns a Collection object 
        '''
        url_request_string = self._baseurl_collections[0:(len(self._baseurl_collections)-2)] + f"/{collection_slug}"
        result = self._make_request(url_request_string, 'get_collection_single')            
        #FIXME: Check collection is actually got something, otherwise just return an empty dict?            
        return Collection(result['collection']) 

    #REF: https://docs.opensea.io/reference/retrieving-collection-stats 
    def get_collection_stats(self, collection_slug):
        '''
        Pass in the collection)slug for a given collection. Returns a Collection object 
        '''
        url_request_string = self._baseurl_collections[0:(len(self._baseurl_collections)-2)] + f"/{collection_slug}/stats"
        result = self._make_request(url_request_string, 'get_collection_stats')            
        return CollectionStats(result['stats']) 
    
    def _write_json(self, file_name, data):
        '''
        Private class used for writing .json files out to a folder called 'api-responses/' This is useful for debugging
        Optionally Called by _make_request()
        '''
        timestamp = str(datetime.now())
        file_path: str = "api-responses/"+file_name+'-'+timestamp+'.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)