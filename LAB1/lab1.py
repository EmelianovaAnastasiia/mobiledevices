import csv


def lab1():
    file = open('data.csv', 'r')
    table = csv.DictReader(file, delimiter=",")
    number = "915642913"
    call_price = 1
    call_duration = 0
    free_sms = 5
    sms1 = 5
    sms1price = 1
    sms2price = 2
    finalprice = 0
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
    print("Итоговая стоимость: {0} руб".format(finalprice))


if __name__ == '__main__':
    lab1()