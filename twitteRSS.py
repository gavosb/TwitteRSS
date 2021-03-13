# Twitter RSS Feed script
# By Gavin
#
# February 24 2021

import twint
import PyRSS2Gen
import datetime
import json
import os

# Acquires twitter feed json from API
class twitter_feed():
	def __init__(self, username, limit):
		self.username = username
		self.c = twint.Config()
		self.c.Username = username
		#config.Profile_full = True #uncomment if user is shadowbanned
		self.limit = limit
		self.c.Store_json = True 
		self.c.Output = "temp.json"
		self.jsonfile = []
		
	def get_Posts(self):
		if self.limit != 0: # 0 is no limit
			self.c.Limit = self.limit
		twint.run.Search(self.c)
	
	def get_Rss_Bit(self, index):
		
		item = PyRSS2Gen.RSSItem(
		title = "Twitter post by " + index["username"],
		link = index["link"],
		description = index["tweet"],
		guid = PyRSS2Gen.Guid(index["link"]),
		pubDate = index["date"] + " " + index["time"] + " " + index["timezone"])
		
		return item
	
	# Converts RSS bits and returns full RSS XML output
	def convert_RSS(self):
		bitlist = []
			
		#main xml
		
		with open('temp.json') as fp:
			for line in fp:
				self.jsonfile.append(json.loads(line))
				print(type(line))
		
		for i in self.jsonfile:
			bitlist.append(self.get_Rss_Bit(i))
		
		rss = PyRSS2Gen.RSS2(
		title = "Twitter feed of " + self.username,
		link = "https://www.twitter.com/" + self.username,
		description = self.username + " feed",
		lastBuildDate = datetime.datetime.now(),
		items = bitlist)
		
		rss.write_xml(open("twitter_" + self.username + ".xml", "w"))
		
		#clean up leftover files
		if os.path.exists("temp.json"):
			os.remove("temp.json")


#test
#twiddle = twitter_feed("username", 100)
#twiddle.get_Posts()
#twiddle.convert_RSS()
