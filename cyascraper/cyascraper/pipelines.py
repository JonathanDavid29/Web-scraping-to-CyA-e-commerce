# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class CyascraperPipeline:
    def process_item(self, item, spider):
        """
        Create an adapter to access and modify the item more easily.
        """
        adapter = ItemAdapter(item)

        ## availability -> extract the items in stock
        item_availability = adapter.get('availability')
        adapter['availability'] = item_availability.split('/')[3]

        ## description -> Delete html tags and merge all list into one
        item_description = adapter.get('description')
        description_cleaned = ''.join(re.sub(r'<br>|<p>|</p>', ' ', item_description))
        adapter['description'] = description_cleaned

        ##price -> convert to float 
        item_price = adapter.get('price')
        adapter['price'] = float(item_price)

        return item
