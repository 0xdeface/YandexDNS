__author__ = 'deface'
from urllib import request, parse
import json
import logging
import re


class YandexDNS(object):
    # API URLS
    host = "https://pddimp.yandex.ru/api2/admin/dns/"
    request = ""
    response = ""
    records = []


    def __init__(self, domain, token):
        self.domain = domain
        self.token = token
        logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                            filename='dns_updater.log')
        self._get_records()


    def _send(self, url, data=None):
        try:
            if data is not None:
                data = parse.urlencode(data).encode("utf-8")
            req = request.Request(self.host + url, data, {'PddToken': self.token})
            resp = request.urlopen(req).read().decode("utf-8")
            return json.loads(resp)
        except:
            logging.critical("Ошибка при отправке запроса")


    def update(self, data, query=None, custom=None):
        if custom is not None and len(custom):
            records = custom
        else:
            records = self.records
        if query is not None:
            records = self._query(query)

        for rec in records:
            for key in data.keys():
                rec[key] = data[key]
            logging.info("Обновляем запись" + rec[key])
            self._send("edit", rec)

    def list(self, query):
        if query is not None:
            return self._query(query)
        return self.records

    def _get_records(self):
        response = self._send("list?domain=" + self.domain)
        self.records = response['records']

    def _query(self, query):
        result = []
        match = True
        for rec in self.records:
            for key in query.keys():
                try:
                    if rec[key].strip() != query[key].strip():
                        match = False
                except(KeyError, IndexError):
                    match = False
                    continue
            if match:
                result.append(rec)
            match = True

        return result

    def add(self, record):
        if "type" not in record.keys() or "content" not in record.keys():
            raise Exception("type or content not found in record")
        self._send("add", record)

    def delete(self):
        pass

    @staticmethod
    def get_my_ip():
        sources = [{"ip": "http://api.ipify.org/?format=json"},
                   {"ip_addr": "http://ifconfig.me/all.json", },
                   {"ip": "http://www.trackip.net/ip?json"}]

        for source in sources:
            for key in source.keys():
                try:
                    response = request.urlopen(source[key], timeout=5).read().decode("utf-8")
                    parsed = json.loads(response)
                    ip = parsed[key]
                    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
                    test_ip = re.compile(pattern)
                    if test_ip.match(ip):
                        return ip
                except:
                    logging.warning(u"не доступен: " + source[key])


