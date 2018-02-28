# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os


class MbedParserPipeline(object):
    def print_item(self, lib_info):
        print(json.dumps(
            lib_info,
            indent=4,
            sort_keys=True,
            separators=(',', ': '),
            ensure_ascii=False))

    def write_to_json_file(self, json_item):
        path = os.path.dirname(os.path.realpath(__file__))
        repo_tokens = json_item['repository']['url'].split('/')
        with codecs.open(
                path + '/configs/' + repo_tokens[6] + "_" + repo_tokens[4] +
                ".json",
                "w",
                encoding='utf-8') as f:
            print("####################  >>>  ",
                  repo_tokens[6] + "_" + repo_tokens[4] + ".json")
            json.dump(
                dict(json_item),
                f,
                indent=4,
                sort_keys=True,
                separators=(',', ': '),
                ensure_ascii=False)

    def process_item(self, item, spider):
        json_item = {}
        json_item['authors'] = {}
        json_item['authors']['name'] = item['author_name']
        json_item['authors'][
            'url'] = "https://os.mbed.com" + item['author_url']
        if item['dependencies']:
            json_item['dependencies'] = item['dependencies']

        if item['examples']:
            json_item['examples'] = item['examples']
        json_item['frameworks'] = 'mbed'
        json_item['name'] = item['name']
        if 'description' in item:
            json_item['description'] = item['description']
        else:
            json_item['description'] = item['name']
        if 'keywords' in item:
            json_item['keywords'] = item['keywords']
        else:
            json_item['keywords'] = json_item['name']
        json_item['platforms'] = "*"
        json_item['repository'] = {}
        json_item['repository']['type'] = 'hg'
        json_item['repository'][
            'url'] = "https://os.mbed.com" + item['repo_url']
        self.print_item(json_item)
        self.write_to_json_file(json_item)
