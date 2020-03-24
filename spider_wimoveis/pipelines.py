# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class WimoveisSqlitePipeline(object):
    
    def process_item(self, item, spider):
        spider.log('------- ITEM CAPTURADO -------')
        self.conn.execute(
            'insert into imoveis(titulo, desc, end, area_tot, area_util, banheiros, quartos, vagas, suites, idade_imovel, preco, imob, tpo_publicado, cod, url, coordinates) values (:titulo, :desc, :end, :area_tot, :area_util, :banheiros, :quartos, :vagas, :suites, :idade_imovel, :preco, :imob, :tpo_publicado, :cod, :url, :coordinates)', item)
        self.conn.commit()
        return item
    
    def create_table(self):
        result = self.conn.execute('select name from sqlite_master where type = "table" and name = "imoveis"')
        try:
            value = next(result)
        except StopIteration as ex:
            self.conn.execute(
                'create table imoveis(id integer primary key, titulo text, desc text, end text, area_tot text, area_util text, banheiros text, quartos text, vagas text, suites text, idade_imovel text, preco text, imob text, tpo_publicado text, cod text, url text, coordinates text)')

    def open_spider(self, spider):
        self.conn = sqlite3.connect('db.sqlite3')
        self.create_table()
    
    def close_spider(self, spider):
        self.conn.close()
