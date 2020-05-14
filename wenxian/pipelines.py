# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import os
from datetime import datetime
from wenxian import settings

class WenxianFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        super(WenxianFilesPipeline, self).file_path(request, response, info)
        date_path = os.path.join(settings.FILES_STORE, str(datetime.date(datetime.now())))
        if not os.path.exists(date_path):
            os.mkdir(date_path)
        file_name = request.item['name']
        file_path = os.path.join(date_path, file_name)
        return file_path

    def get_media_requests(self, item, info):
        request_objs = super(WenxianFilesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs
