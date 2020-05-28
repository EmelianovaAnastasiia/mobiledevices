import csv
import datetime
from math import ceil
from docx2pdf import convert
from docxtpl import DocxTemplate

ip_given = "192.168.250.59"
price_after_500 = 1
price_before_500 = 0.5

information = {
    'poluchatel': {
        'name': 'Емельянова Анастасия Витальевна',
        'address': '167002, г. Санкт-Петербург, ул. Апрельская, д. 24, кв. 50',
        'account': '5555555555',
        'inn': '4444444444',
        'kpp': '9999999999',
        'bank': {
            'name': 'СБЕР"',
            'bik': '85777885489',
            'account': '868965695869'
        },
        'ceo': 'Булкина ИА',
        'buch': 'Сергеева АВ'
    },
    'zakazchik': {
        'name': 'Беляев СБ',
        'inn': '78868674389',
        'kpp': '8548549590',
        'address': '190167, г. Санкт-Петербург, ул. Малая Конюшенная, д.56, кв. 11'
    },
    'payment': {
        'id': '1',
        'date': '23.05.2020',
        'sum': '',
        'nds': '',
        'cause': 'платеж от 23.05.2020',
        'uslugi': ''
    },
    'uslugi': [
        {
            'id': '1',
            'name': 'Звонки и СМС',
            'amount': '-',
            'measure': '-',
            'price': '-',
            'sum': ''
        },
        {
            'id': '2',
            'name': 'Интернет',
            'amount': '',
            'measure': 'Кб',
            'price': "До 500 Кб - {0} руб/Кб, после - {1} руб/Кб".format(price_before_500, price_after_500),
            'sum': ''
        }
    ]
}

sample = 'sample.docx'
result = 'Счет №{0} от {1}.docx'.format(information['payment']['id'], information['payment']['date'])

number = "915642913"
call_price = 1

free_sms = 5
sms1 = 5
sms1price = 1
sms2price = 2


def lab1():
    call_duration = 0
    finalprice = 0
    file = open('data.csv', 'r')
    table = csv.DictReader(file, delimiter=",")

    for data in table:
        if (data['msisdn_origin'] == number) or (data['msisdn_dest'] == number):
            call_duration += float(data['call_duration'])
            finalprice += call_duration * call_price
            call_duration = 0
            if data['msisdn_origin'] == number:
                sms_number = int(data['sms_number'])
                if sms_number > free_sms:
                    sms = sms_number - free_sms
                    if sms > sms1:
                        sms = (sms - sms1) * sms2price + sms1 * sms1price
                    else:
                        sms = sms * sms1price
                else:
                    sms = 0
    finalprice += sms
    file.close()
    information['uslugi'][0]['sum'] = finalprice
    return finalprice

lab1()

file = open('LAB2.csv', 'r')


def lab2():
    file = open('LAB2.csv', 'r')
    amount = 0

    table = csv.DictReader(file, delimiter=",")
    data = []
    for row in table:
        if row['da'] == ip_given:
            amount += int(row['ibyt'])

            if row['ts'] == "Summary":
                break
            else:
                i = (datetime.datetime.strptime(row['ts'], '%Y-%m-%d %H:%M:%S'), int(row['ibyt']))
                data.append(i)


    amount = ceil(amount * 8 / 2**10)


    if amount > 500:
        total = (price_before_500 * 500) + (price_after_500 * (amount-500))
    else:
        total = price_before_500 * amount

    information['uslugi'][1]['amount'] = amount
    information['uslugi'][1]['sum'] = total
    return total

file.close()

lab2()

def lab3():
    finalprice = lab1()
    total = lab2()

    information['payment']['sum'] = total + finalprice
    information['payment']['nds'] = (total + finalprice) * 0.2
    information['payment']['uslugi'] = len(information['uslugi'])

    doc = DocxTemplate(sample)
    doc.render(information)
    doc.save(result)
    convert(result)

lab3()
