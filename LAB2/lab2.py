import csv
import datetime
from math import ceil
import matplotlib.pyplot as plt


file = open('LAB2.csv', 'r')

def lab2():
    file = open('LAB2.csv', 'r')
    amount = 0
    ip_given = "192.168.250.59"
    price_after_500 = 1
    price_before_500 = 0.5
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

    print("IP-адрес 192.168.250.59 использовал {0}Kb.\nИтоговая стоимость: {1} рублей.".format(amount, total))




    data_sorted = sorted(data, key=lambda time: time[0])
    amount_of_bytes = []
    time = []
    for i in data_sorted:
        amount_of_bytes.append(i[1] * 8 / (2**10))
        time.append(i[0])

    fig, graph = plt.subplots()
    graph.plot(time, amount_of_bytes, label='Traffic usage in Mb')
    graph.legend(loc='upper left')
    graph.set_xlabel('Время')
    graph.set_ylabel('Кб')
    graph.set_title('График зависимости объема трафика от времени')
    plt.savefig('plot.png')
    plt.show()


file.close()

lab2()
