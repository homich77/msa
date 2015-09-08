import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "extract_data.settings")

from main.models import MainData, City, Proxy


class ScrapPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'msa':
            link = item['link']
            index = link.find('//') + 2
            city_name = link[index:].split('.')[0]
            city, created = City.objects.get_or_create(name=city_name)

            db_data = MainData.objects.filter(link=item['link']).first()
            if not db_data:
                MainData.objects.create(city=city, **item)
            elif not db_data.email and item['email']:
                db_data.email = item['email']
                db_data.save()
            if db_data and not db_data.phone and item['phone']:
                db_data.phone = item['phone']
                db_data.save()
            return item
        else:
            item['address'] = 'http://%s' % item['address']
            Proxy.objects.get_or_create(address=item['address'])
