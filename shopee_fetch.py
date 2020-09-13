import time
import requests
import json
from tqdm import tqdm
import constant_file

# YOU COULD ALSO ADD SOME ATTRIBUTE ON YOUR OWN.
class product(object):
    name = 'name'
    price = 1
    weblink = 'weblink'
    photo_count = 0
    photolinks = []
    avg_rating = 4.0
    rating_count_list = [] #[total, 1, 2, 3, 4, 5]

def getAllItems(keyword, n_items = 30, minPrice = 1, maxPrice = 200000000, locations = '', ratingFilter = 0, preferred = False, officialMall = False):
    print(str.lower(str(preferred)))
    search_url = f'https://shopee.tw/api/v1/search_items/\
?by=relevancy\
&locations={locations}\
&keyword={keyword}\
&limit={n_items}\
&locations={locations}\
&ratingFilter={ratingFilter}\
&preferred={str.lower(str(preferred))}\
&officialMall={str.lower(str(officialMall))}'


    search_result = requests.get(search_url, headers = constant_file.headers)
    search_data = json.loads(search_result.text)
    product_list = []

    for i in tqdm(range(n_items), desc = 'Processing search data...'):
        product_list.append({'shopid':search_data['items'][i]['shopid'], 
            'itemid':search_data['items'][i]['itemid']})
    return product_list


def getItemInfo(itemid, shopid):
    product_object = product()
    product_url = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
    product_info = requests.get(product_url, headers = constant_file.headers)
    
    product_data = json.loads(product_info.text)

    '''
    Description: For each Product, you will need attributes 'name', 'price', 
    'weblink', 'photo_count, 'photolinks (list)', 'avg_rating', 'rating_count_list'
    for each product. Try to find each corresponding info in the example json file.
    Note: There is some tricky thing with product price.
    '''
    setattr(product_object, 'name', product_data['item']['name'])
    setattr(product_object, 'price', product_data['item']['price'])
    setattr(product_object, 'weblink', f'https://shopee.tw/product/{shopid}/{itemid}')
    setattr(product_object, 'photo_count', len(product_data['item']['images']))
    setattr(product_object, 'photolinks', 
        [f'https://cf.shopee.tw/file/{photo_hash}' for photo_hash in product_data['item']['images']])
    setattr(product_object, 'avg_rating', product_data['item']['item_rating']['rating_star'])
    setattr(product_object, 'rating_count_list', product_data['item']['item_rating']['rating_count'])
    
    time.sleep(0.15) # to avoid of being recognized as robot by shopee server
    return product_object
    
def main():
    # Testing functions
    product_list = getAllItems(keyword = 'iPhone 11', n_items = 40, locations = -1, ratingFilter = 4)
    #print("itemid = ", product_list[0]['itemid'], "shopid = ", product_list[0]['shopid'])
    product_object = getItemInfo(product_list[0]['itemid'], product_list[0]['shopid'])
    print("name = ", product_object.name)
    print("price = ", product_object.price / 1e5)
    print("weblink = ", product_object.weblink)
    print("photo_count = ", product_object.photo_count)
    print("avg_rating = ", product_object.avg_rating)
    print("rating_count_list = ", product_object.rating_count_list)

    # Simple Filters
    '''
    keyword: <str>
    n_items: <positive int>
    '''

    '''
    locations:
        -1 : Taiwan
        -2 : Abroad
    '''

    '''
    ratingFilter: <positive int>
    preferred = <bool> 蝦皮優選賣家
    officialMall = <bool> 蝦皮商城賣家
    '''

if __name__ == '__main__':
    main()