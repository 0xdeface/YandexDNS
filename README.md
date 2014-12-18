# Yandex DNS API v2

This script implements basic function to manage your DNS records with YandexPDD DNS API
  - get records with query 
  - update records with query
  - add new records

## Basic usage
    if __name__ == '__main__':
        domains = {'domain.pro': 'TOKENTOKENUZT262YVD6S24RASKVT3FILR3RXDUSYEWXAJ6CIOQ',
                 'domain.ru': 'TOKENTOKETOKWCF4S63NLKACP52PVKG4TR3LRCOAMM5QKVPLST5A',
        }
        ip = YandexDNS.get_my_ip()
        for domain in domains.keys():
            yad = YandexDNS(domain, domains[domain])
            rec = yad.list({'type': 'A'})
            for r in rec:
                if r["content"] != ip:
                    yad.update({'content': ip}, {'type': 'A'})

this code get all records TYPE:A and update IP adres. I use this for my Dynamic DNS server.
I add this script to crontab to execute every hours

