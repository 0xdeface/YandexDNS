# Yandex DNS API v2
Скрипт реализует базовые функции по управлению вашими DNS записями над доменами передаными
яндексу (http://pdd.yandex.ru)

Получить токены для доменов можно по этому адресу https://pddimp.yandex.ru/api2/admin/get_token
## Базовый функционал
  - Получение записей по запросу
  - Обновление записей по запросу
  - Добавление новых записей
  - Получение внешнего адреса из нескольких источников
  - Логирование недоступных источников, смен адреса и проблем с АПИ

## Пример использования
    if __name__ == '__main__':
        domains = {'domain.pro': 'TOKENTOKENUZTghDSFSDFAJ6CIOQ',
                 'domain.ru': 'TOKENTOKETOKWCF4S63NВАЫАЫВАOAMM5QKVPLST5A',
        }
        ip = YandexDNS.get_my_ip()
        for domain in domains.keys():
            yad = YandexDNS(domain, domains[domain])
            rec = yad.list({'type': 'A'})
            for r in rec:
                if r["content"] != ip:
                    yad.update({'content': ip}, {'type': 'A'})

Этот код получает все записи с TYPE:A и обновлят для них IP адрес. 
Я испольхую этот скрипт для работы с домашним сервером для разработки, он исправно служит мне уже больше полугода.

