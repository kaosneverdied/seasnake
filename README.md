# seasnake
Python wrapper for OpenSea's free API. the module turns .json data into python objects making it easer and cleaner to work with OpenSea data.  

**This is a work in progress**

## How to Setup in your porject:
Add `seasnake.py` to your project folder and import it into the file you want to acces it from with `from seasnake import *`. It is also advsed that you import they typing library to assist with code prompting

**Important:** seasnake has utilises logging to aid with devleopment and debugging. In whichever file you imported seasnake also import logging by adding `import logging` then add the following code: 

```python

logger = logging.getLogger()
logger.setLevel(logging.INFO) #NOTE: minimum logging level - set this to whatever suits your needs

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
```

## Methods and Classes
Importing seasnake gives you access to object based interface for the OpenSea Free API. An opensea object may be creaed as follows:  
`opensea = OpenSea()`

### Methods
This object may then use the following methods to retireve data from openSea. The data is rendered into Object form for ease of handling. Current methods implimented are given below with their return types.   
* `get_assets() -> List[Asset]`
* `get_events() -> List[Event]`
* `get_collections() -> List[Collection]`
* `get_bundles() -> List[Bundle]`
* `get_asset_single() -> Asset`
* `get_contract_single() -> Contract`
* `get_collection_single() -> Collection`
* `get_collection_stats -> CollectionStats`

**NOTE:** Each of the above methods has a range of parameter variables that can be passed to it to refine the search criteria. Please examine the code to understand what these are. If you have imported pythons tpying library then your code prompt shoudl hint these. Please specify using `parameter_name = paramater_data`. 

## Example
The following creates an opensea object which is then used to get a Collection object named 'official':
```python
opensea = Opensea()
offical_collection = opensea.get_collection_single(collection_slug='official')
```
Once the object has been retrieved it can be accessed via the class variables. A complete list of these is given below for each object class. 

### Classes:
* Asset
    * id -> int
    * token_id -> str
    * num -> int
    * background_color -> str
    * image_url -> str
    * image_preview_url -> str
    * image_thumbnail_url -> str
    * image_original_url -> str
    * animation_url -> str
    * animation_original_url -> str
    * name -> str
    * description -> str
    * external_link -> str
    * asset_contract -> Contract Object (see Contract for attributes)
    * permalink -> str
    * collection -> Collection Object (see Collection for attributes)
    * decimals -> int
    * token_metadata -> str
    * owner -> Owner Object (see Stakeholder for attributes)
    * sell_orders
    * creator -> Creator Object (see Stakeholder for attributes)
    * traits -> Traits Object (see Traits object for attributes)
    * last_sale -> ?
    * top_bid -> ?
    * listing_date -> ?
    * is_presale -> ?
    * transfer_fee_payment_token -> ?


* Stakeholder (same method sfor Owner, Creator, Seller, FromAccount) 
    * user -> dict
    * profileImg_url -> str
    * address -> str
    * config -> str

**Important Note:** The Traits class may be removed soon as recent tests show variance in the strcuture of traits across different returned data sets.  
* Traits
    * trait_type -> str
    * value -> str
    * display_type -> str
    * max_value -> ?
    * trait_count -> int
    * order -> ?


* Event
    * approved_account -> str
    * asset -> Asset Object (see Asset for attributes)
    * asset_bundle -> ?
    * auction_type -> str
    * bid_amount -> ?
    * collection_slug -> str
    * contract_address -> str
    * created_date -> str
    * custom_event_name -> str
    * dev_fee_payment_event -> ?
    * duration -> str
    * ending_price -> str
    * event_type -> str
    * FromAccount -> FromAccount Object (see Stakeholder for attributes)
    * id -> int
    * is_private -> boolean
    * owner_account -> ?
    * payment_token -> PaymentToken Object (see PaymentToken for attributes)
    * quantity -> str
    * seller -> Seller Object (see Stakeholder for attributes)
    * starting_price -> str
    * to_account -> str
    * total_price -> str
    * transaction -> str
    * winner_account -> str

* PaymentToken
    * id -> int
    * symbol -> str
    * address -> str
    * image_url -> str
    * name -> str
    * decimals -> int
    * eth_price -> str
    * usd_price -> str

* Collection
    * primary_asset_contracts ->  list
    * traits -> dict
    * stats -> CollectionStats Object (see CollectionStats for attributes)    
    * banner_image_url -> str 
    * chat_url -> str
    * created_date -> str
    * default_to_fiat -> boolean
    * description -> str
    * dev_buyer_fee_basis_points -> str 
    * dev_seller_fee_basis_points -> str
    * discord_url -> str
    * display_data -> dict   
    * external_url -> str
    * featured -> boolean
    * featured_image_url -> str   
    * hidden -> boolean
    * safelist_request_status -> str  
    * image_url -> str 
    * is_subject_to_whitelist -> boolean
    * large_image_url -> str
    * medium_username -> str
    * name -> str 
    * only_proxied_transfers -> boolean
    * opensea_buyer_fee_basis_points -> str
    * opensea_seller_fee_basis_points -> str
    * payout_address -> str
    * require_email -> boolean
    * short_description -> str
    * slug -> str
    * telegram_url -> str
    * twitter_username -> str
    * instagram_username -> str
    * wiki_url -> str

* CollectionStats
    * one_day_volume -> float
    * one_day_change -> float
    * one_day_sales -> float
    * one_day_average_price -> float
    * seven_day_volume -> float
    * seven_day_change -> float
    * seven_day_sales -> float
    * seven_day_average_price -> float
    * thirty_day_volume -> float
    * thirty_day_change -> float
    * thirty_day_sales -> float
    * thirty_day_average_price -> float
    * total_volume -> float
    * total_sales -> float
    * total_supply -> float
    * count -> float
    * num_owners -> float
    * average_price -> float
    * num_reports -> float
    * market_cap -> float
    * floor_price -> float

The following example illustrates how to will retireve a single Asset and access some of its attributes
 
```python
asset_contract_address = "0x06012c8cf97bead5deae237070f9587f8e7a266d"
token_id = "1"
opensea = OpenSea()
asset = opensea.get_asset_single(asset_contract_address=asset_contract_address, token_id=token_id)
print(f'id: {asset.id}')
print(f'token_id: {asset.token_id}')
print(f'background_color: {asset.background_color}')
print(f'img_url: {asset.image_url}')
```
