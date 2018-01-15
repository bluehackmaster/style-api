import os
import time
import redis
import pickle
from bluelens_log import Logging
from swagger_server.models.get_images_response import GetImagesResponse
from swagger_server.models.get_image_response import GetImageResponse
from swagger_server.models.image import Image
from stylelens_index.indexes import Indexes

from .search import Search

REDIS_INDEXED_IMAGE_HASH = 'bl_indexed_image_hash'
REDIS_INDEXED_IMAGE_HASH_MAP = 'bl_indexed_image_hash_map'
REDIS_INDEXED_IMAGE_LIST = 'bl:indexed:image:list'
REDIS_INDEXED_OBJECT_HASH = 'bl_indexed_object_hash'
REDIS_INDEXED_OBJECT_HASH_MAP = 'bl_indexed_object_hash_map'
REDIS_INDEXED_OBJECT_LIST = 'bl:indexed:object:list'

REDIS_SERVER = os.environ['REDIS_SEARCH_SERVER']
REDIS_PASSWORD = os.environ['REDIS_SEARCH_PASSWORD']

REDIS_SEARCH_OBJECT_SERVER_0 = os.environ['REDIS_SEARCH_OBJECT_SERVER_0']
REDIS_SEARCH_OBJECT_PASSWORD_0 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_0']
REDIS_SEARCH_OBJECT_SERVER_1 = os.environ['REDIS_SEARCH_OBJECT_SERVER_1']
REDIS_SEARCH_OBJECT_PASSWORD_1 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_1']
REDIS_SEARCH_OBJECT_SERVER_2 = os.environ['REDIS_SEARCH_OBJECT_SERVER_2']
REDIS_SEARCH_OBJECT_PASSWORD_2 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_2']
REDIS_SEARCH_OBJECT_SERVER_3 = os.environ['REDIS_SEARCH_OBJECT_SERVER_3']
REDIS_SEARCH_OBJECT_PASSWORD_3 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_3']
REDIS_SEARCH_OBJECT_SERVER_4 = os.environ['REDIS_SEARCH_OBJECT_SERVER_4']
REDIS_SEARCH_OBJECT_PASSWORD_4 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_4']
REDIS_SEARCH_OBJECT_SERVER_5 = os.environ['REDIS_SEARCH_OBJECT_SERVER_5']
REDIS_SEARCH_OBJECT_PASSWORD_5 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_5']
REDIS_SEARCH_OBJECT_SERVER_6 = os.environ['REDIS_SEARCH_OBJECT_SERVER_6']
REDIS_SEARCH_OBJECT_PASSWORD_6 = os.environ['REDIS_SEARCH_OBJECT_PASSWORD_6']
OBJECT_HASH_RANGE_0 = 0
OBJECT_HASH_RANGE_1 = 1
OBJECT_HASH_RANGE_2 = 2
OBJECT_HASH_RANGE_3 = 3
OBJECT_HASH_RANGE_4 = 4
OBJECT_HASH_RANGE_5 = 5
OBJECT_HASH_RANGE_6 = 6

REDIS_SEARCH_IMAGE_SERVER_0   = os.environ['REDIS_SEARCH_IMAGE_SERVER_0']
REDIS_SEARCH_IMAGE_PASSWORD_0 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_0']
REDIS_SEARCH_IMAGE_SERVER_1   = os.environ['REDIS_SEARCH_IMAGE_SERVER_1']
REDIS_SEARCH_IMAGE_PASSWORD_1 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_1']
REDIS_SEARCH_IMAGE_SERVER_2   = os.environ['REDIS_SEARCH_IMAGE_SERVER_2']
REDIS_SEARCH_IMAGE_PASSWORD_2 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_2']
REDIS_SEARCH_IMAGE_SERVER_3   = os.environ['REDIS_SEARCH_IMAGE_SERVER_3']
REDIS_SEARCH_IMAGE_PASSWORD_3 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_3']
REDIS_SEARCH_IMAGE_SERVER_4   = os.environ['REDIS_SEARCH_IMAGE_SERVER_4']
REDIS_SEARCH_IMAGE_PASSWORD_4 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_4']
REDIS_SEARCH_IMAGE_SERVER_5   = os.environ['REDIS_SEARCH_IMAGE_SERVER_5']
REDIS_SEARCH_IMAGE_PASSWORD_5 = os.environ['REDIS_SEARCH_IMAGE_PASSWORD_5']
IMAGE_HASH_RANGE_0 = 0
IMAGE_HASH_RANGE_1 = 1
IMAGE_HASH_RANGE_2 = 2
IMAGE_HASH_RANGE_3 = 3
IMAGE_HASH_RANGE_4 = 4
IMAGE_HASH_RANGE_5 = 5

CACHE_MAX_NUM = 7000

rconn = redis.StrictRedis(REDIS_SERVER, decode_responses=False, port=6379, password=REDIS_PASSWORD)

rconn_search_object_0 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_0, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_0)
rconn_search_object_1 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_1, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_1)
rconn_search_object_2 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_2, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_2)
rconn_search_object_3 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_3, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_3)
rconn_search_object_4 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_4, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_4)
rconn_search_object_5 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_5, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_5)
rconn_search_object_6 = redis.StrictRedis(REDIS_SEARCH_OBJECT_SERVER_6, port=6379, password=REDIS_SEARCH_OBJECT_PASSWORD_6)

rconn_search_image_0 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_0, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_0)
rconn_search_image_1 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_1, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_1)
rconn_search_image_2 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_2, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_2)
rconn_search_image_3 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_3, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_3)
rconn_search_image_4 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_4, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_4)
rconn_search_image_5 = redis.StrictRedis(REDIS_SEARCH_IMAGE_SERVER_5, port=6379, password=REDIS_SEARCH_IMAGE_PASSWORD_5)
options = {
  'REDIS_SERVER': REDIS_SERVER,
  'REDIS_PASSWORD': REDIS_PASSWORD
}
log = Logging(options, tag='style-api:Products')

class Images(object):
  def __init__(self):
    super().__init__()

  @staticmethod
  def get_images(image_id, offset, limit):
    log.info('get_images_by_id')
    start_time = time.time()
    index_api = Indexes()
    res = GetImageResponse()

    try:
      image_d = rconn.hget(REDIS_INDEXED_IMAGE_HASH, image_id)

      if image_d != None:
        image_dic = pickle.loads(image_d)
      else:
        image_dic = index_api.get_image(image_id)

      image_dic['id'] = str(image_dic['_id'])
      image_dic.pop('_id')
      img = Image()
      image = img.from_dict(image_dic)

      res.data = image.images
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status

  @staticmethod
  def get_image_from_cache(image_id):
    hash_range = rconn.hget(REDIS_INDEXED_IMAGE_HASH_MAP, image_id)
    if hash_range == IMAGE_HASH_RANGE_0:
      rconn_search_image_0.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
    elif hash_range == IMAGE_HASH_RANGE_1:
      rconn_search_image_1.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
    elif hash_range == IMAGE_HASH_RANGE_2:
      rconn_search_image_2.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
    elif hash_range == IMAGE_HASH_RANGE_3:
      rconn_search_image_3.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
    elif hash_range == IMAGE_HASH_RANGE_4:
      rconn_search_image_4.hget(REDIS_INDEXED_IMAGE_HASH, image_id)
    elif hash_range == IMAGE_HASH_RANGE_5:
      rconn_search_image_5.hget(REDIS_INDEXED_IMAGE_HASH, image_id)

  @staticmethod
  def get_images_by_user_image_file(file, offset=0, limit=5):
    search = Search(log)
    res = GetImagesResponse()
    start_time = time.time()

    try:
      images = search.search_user_image_file(file, offset, limit)

      res.message = 'Successful'
      res.data = images

      response_status = 200
    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('get_images_by_user_image_file time: ' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_images_by_user_image_id_and_object_index(user_image_id, object_index):
    log.info('get_images_by_user_image_id_and_object_index')
    start_time = time.time()
    index_api = Indexes()
    res = GetImagesResponse()
    log.debug(user_image_id)
    log.debug(object_index)

    try:
      api_res = index_api.get_images_by_user_image_id_and_object_index(user_image_id, object_index)
      res.message = 'Successful'
      images = []
      for p in api_res.data:
        images.append(p.to_dict())
      res.data = images
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('time: get_images_by_user_image_id_and_object_index' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_image_by_host_code_and_product_no(host_code, product_no):
    log.info('get_image_by_host_code_and_product_no')
    start_time = time.time()
    index_api = Indexes()
    res = GetImageResponse()
    image = Image()

    try:
      api_res = index_api.get_image_by_hostcode_and_product_no(host_code, product_no)
      res.data = image.from_dict(api_res.data.to_dict())
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    elapsed_time = time.time() - start_time
    log.info('time: get_image_by_host_code_and_product_no' + str(elapsed_time))
    return res, response_status

  @staticmethod
  def get_image_by_id(image_id):
    log.info('get_image_by_id')
    start_time = time.time()
    index_api = Indexes()
    res = GetImageResponse()

    try:


      image_d = rconn.hget(REDIS_INDEXED_IMAGE_HASH, image_id)

      if image_d != None:
        image_dic = pickle.loads(image_d)
      else:
        image_dic = index_api.get_image(image_id)

      image_dic['id'] = str(image_dic['_id'])
      image_dic.pop('_id')
      img = Image()
      image = img.from_dict(image_dic)

      res.data = image
      res.message = 'Successful'
      response_status = 200

    except Exception as e:
      log.error(str(e))
      response_status = 400

    return res, response_status