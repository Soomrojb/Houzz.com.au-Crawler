# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import urllib2, requests

GoogleURL = "https://script.google.com/macros/s/AKfycbya3T7dcbunoow22WfI0jtyJYvUIYa8fW0vgs8A3vP0YOFfUqvu/exec"

class HouzzPipeline(object):
    
    def __init__(self):
        self.SetupDBConn()

    def SetupDBConn(self):
        self.Conn = sqlite3.connect("db/houzz.db")
        self.Cursor = self.Conn.cursor()
        self.Cursor.execute('CREATE TABLE IF NOT EXISTS houzz ' \
            '(id INTEGER PRIMARY KEY, \
            category VARCHAR(80), \
            posttitle VARCHAR(80), \
            posthref VARCHAR(80), \
            location VARCHAR(80), \
            contact VARCHAR(80), \
            phone VARCHAR(80))')
        print "Sqlite3 connection successfull!"

    def process_item(self, item, spider):
        category = item['category']
        posttitle = item['posttitle']
        posthref = item['posthref']
        location = item['location']
        contact = item['contact']
        phone = item['phone']
        # Queries
        insquery = "INSERT INTO houzz (category, posttitle, posthref, location, contact, phone) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (category, posttitle, posthref, location, contact, phone)
        srcquery = "SELECT * FROM houzz WHERE `posttitle` = \"%s\" AND `posthref` = \"%s\"" % (posttitle, posthref)
        self.Cursor.execute(srcquery)
        if self.Cursor.fetchone() is None:
            # Add only new records
            self.Cursor.execute(insquery)
            self.Conn.commit()
            requests.get(GoogleURL, item)
            return item
        else:
            #raise DropItem("######################################### Item already present in the database! #########################################")
            #return item
            pass
