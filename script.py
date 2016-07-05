# def main():
# 	es = Elasticsearch(['https://search-search-jxvug2z72gmuoz6ysdy3rz4z44.us-west-2.es.amazonaws.com'])
# 	es.indices.refresh(index="test-index")

# main()

def connect():
	from elasticsearch import Elasticsearch, RequestsHttpConnection
	from requests_aws4auth import AWS4Auth

	REGION = "us-west-2"
	host = 'search-search-jxvug2z72gmuoz6ysdy3rz4z44.us-west-2.es.amazonaws.com'
	awsauth = AWS4Auth("AKIAIC6D7UKE76OCB6HQ", "/OMQDN2x8+FZyVeIxa7bbtNXswhYB7uIBOkz6rDi", REGION, 'es')

	es = Elasticsearch(
		hosts=[{'host': host, 'port': 443}],
		http_auth=awsauth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
	)
	print(es.info())
	return es



es = connect()



# def index(self, index, doc_type, body, id=None, params=None):
# 	from elasticsearch.client.utils import query_params, _make_path, SKIP_IN_PATH
# 	path = "/"+index+"/"+doc_type+"/1/"+"_mapping"
# 	print(path)
# 	for param in (index, doc_type, body):
# 		if param in SKIP_IN_PATH:
# 			raise ValueError("Empty value passed for a required argument.")
# 	_, data = self.transport.perform_request('POST' if id in SKIP_IN_PATH else 'PUT',
# 		path, params=params, body=body)
# 	# print(_make_path(index, doc_type, id))
# 	print("/"+index+"/"+doc_type+"/"+"_mapping")
# 	return data
# import types
# es.index2 = types.MethodType(index, es)

TMP_FILE_NAME = "temp"

def readFile64(fname):
	import json
	import base64
	with open(fname, "rb") as f:
		file64 = base64.b64encode(f.read())
	return str(file64)

def uploadFile(fname):
	# doc = {
	# 	"attachment" : {
	# 		"properties" : {
	# 			"file" : {
	# 				"type" : "attachment",
	# 				"fields" : {
	# 					"title" : { "store" : "yes" },
	# 					"file" : { "term_vector":"with_positions_offsets", "store":"yes" }
	# 				}
	# 			}
	# 		}
	# 	}
	# }
	doc = {
		"name": fname,
		"content": readFile64(fname)
	}
	# res = es.delete(index="*", doc_type="*", id="*")
	res = es.index(index="test-index", doc_type='file', id=1, body=doc)
	print(res['created'])
	res = es.get(index="test-index", doc_type='file', id=1)
	# print(res['_source'])
	res = es.search(index="test-index", body={"query": {"wildcard": {"content":"*"}}})
	# res = es.search(index="test-index", q='Resume.pdf')
	print("Got %d Hits:" % res['hits']['total'])
	for hit in res['hits']['hits']:
		print(hit["_source"])

	# import urllib2

	# class HeadRequest(urllib2.Request):
	# 	def get_method(self):
	# 		return "HEAD"

	# check if type exists by sending HEAD request to index
	# try:
	# 	urllib2.urlopen(HeadRequest(HOST + '/' + INDEX + '/' + TYPE))
	# except(urllib2.HTTPError, e):
	# 	if e.code == 404:
	# 		print('Index doesnt exist, creating...')

	# 		os.system('curl -X PUT "{}/{}/{}/_mapping" -d'.format(HOST,INDEX,TYPE) + ''' '{
	# 				"attachment" : {
	# 					"properties" : {
	# 						"file" : {
	# 							"type" : "attachment",
	# 							"fields" : {
	# 								"title" : { "store" : "yes" },
	# 								"file" : { "term_vector":"with_positions_offsets", "store":"yes" }
	# 							}
	# 						}
	# 					}
	# 				}
	# 			}' ''')
	# 	else:
	# 		print('Failed to retrieve index with error code - %s.' % e.code)

uploadFile("Resume.pdf")