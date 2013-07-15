import csv
import util
class MovieLens:
	def __init__(self):
		self.ml_to_dbp = dict()
		
	def load_dbpedia_mapping(self,file_path):
		f = open(file_path,'rb')
		try:
			reader = csv.reader(f)
			rownum = 0
			for row in reader:
				if rownum == 0:
					header = row
				else:
					# colnum = 0
					# for col in row:
					# 	print '%s: %s' % (header[colnum], col)
					# 	colnum += 1
					print "row:",row[0], util.url_decode(row[1])
					ml_id = row[0]
					dbp_uri = row[1]
					self.ml_to_dbp[ml_id] = dbp_uri
				rownum += 1
		finally:
			f.close()
