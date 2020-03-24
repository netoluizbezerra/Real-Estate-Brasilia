# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import sys

class LagoSulSpider(scrapy.Spider):
    name = 'lago_sul'
    start_urls = ['http://www.wimoveis.com.br/casas-venda-distrito-federal-goias-q-lago-sul.html']

    def parse(self, response):
        item = response.xpath('//div[contains(@class, "posting-card ")]')
        for url in item:
            url = ('http://www.wimoveis.com.br{0}'.format(url.xpath("./@data-to-posting").extract_first()))
            
            yield scrapy.Request(url=url, callback=self.parse_url)

        #defindo parada
        last_page = response.xpath('//h1[@class="list-result-title"]/b/text()').extract()
        last_page_float = float(last_page[0])
        last_page_float = (last_page_float * 1000) / 20

        current_page = response.request.url
        current_page = re.sub(':443','', current_page.rstrip())

        self.log('VOCÊ ESTÁ NA PAGINA: {}'.format(current_page))

        if current_page == 'https://www.wimoveis.com.br/casas-venda-distrito-federal-goias-q-lago-sul.html':
            url_new = 'https://www.wimoveis.com.br/casas-venda-distrito-federal-goias-pagina-2-q-lago-sul.html'
            yield scrapy.Request(url=url_new, callback=self.parse)
        elif current_page != 'http://www.wimoveis.com.br/casas-venda-distrito-federal-goias-q-lago-sul.html':
            page_num = int((current_page.split("pagina-")[1]).split("-q-lago-su")[0])
            page_num_str = str(page_num + 1)

            if page_num == last_page_float:
                self.log(sys.exit('É HORA DE PARAR'))

            url_new = 'https://www.wimoveis.com.br/casas-venda-distrito-federal-goias-pagina-{}-q-lago-sul.html'.format(page_num_str)
            yield scrapy.Request(url=url_new, callback=self.parse)
            
    def parse_url(self, response):
        logging.info(response.url)
 # endereço:
        end = response.xpath('//hgroup/h2[contains(@class, "location")]/b/text()').extract_first()
        end = '{0}{1}'.format(end, response.xpath('//hgroup/h2[contains(@class, "location")]/span/text()').extract_first())

    # Atributos Principais:
        area_tot = response.xpath('//i[contains(@class, "icon-f icon-f-stotal")]/following-sibling::b/text()').extract_first()
        area_util = response.xpath('//i[contains(@class, "icon-f icon-f-scubierta")]/following-sibling::b/text()').extract_first()
        banheiros = response.xpath('//i[contains(@class, "icon-f icon-f-bano")]/following-sibling::b/text()').extract_first()
        vagas = response.xpath('//i[contains(@class, "icon-f icon-f-cochera")]/following-sibling::b/text()').extract_first()
        quartos = response.xpath('//i[contains(@class, "icon-f icon-f-dormitorio")]/following-sibling::b/text()').extract_first()
        suites = response.xpath('//i[contains(@class, "icon-f icon-f-toilete")]/following-sibling::b/text()').extract_first()
        idade_imovel = response.xpath('//i[contains(@class, "icon-f icon-f-antiguedad")]/following-sibling::b/text()').extract_first()
        
    # URL:
        url = tpo_publicado = response.xpath('//link[contains(@rel, "canonical")]/@href').extract_first()

    # Título:
        titulo = response.xpath('//title/text()').extract_first()
    # Preço:
        preco = response.xpath('//div[contains(@class, "price-items")]/span/text()').extract_first()
        
    # Imobiliária:
        imob = response.xpath('//h3[contains(@class, "publisher-subtitle")]/b/text()').extract_first()  

        
    # Cód. Wimoveis:
        cod = response.xpath('//span[contains(@class, "publisher-code")]/text()').getall() 
        cod = cod[1]
        
    # Tempo de publicação:
        tpo_publicado = response.xpath('//h5[contains(@class, "section-date css-float-r")]/text()').getall() 
        tpo_publicado = tpo_publicado[1]
        
    # Descricao
        desc = ''.join(response.xpath('//*[@id="verDatosDescripcion"]/text()').getall())
        
    # Coordenadas Geograficas
        string = response.xpath('//img[contains(@class, "static-map")]/@src').extract_first()
        coordinates = (string.split("center=")[1]).split("&zoom")[0]
        
        yield {
            'titulo': titulo,
            'desc': desc,
            'end': end,
            'area_tot': area_tot,
            'area_util': area_util,
            'banheiros': banheiros,
            'vagas': vagas,
            'quartos': quartos,
            'suites': suites,
            'idade_imovel': idade_imovel,
            'preco': preco,
            'imob': imob,
            'tpo_publicado': tpo_publicado,
            'cod': cod,
            'url': url,
            'coordinates': coordinates,
        }

