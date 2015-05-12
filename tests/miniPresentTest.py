# coding=utf-8
import pygal
from present.miniPresent import MiniPresent

__author__ = 'Iurii Sergiichuk'

result_file = open('./results.txt', 'w+')


class ResultHolder(object):
    def __init__(self, plain_text, key, encrypted_text):
        self.plain_text = plain_text
        self.key = key
        self.encrypted_text = encrypted_text

    def __unicode__(self):
        return u'plain_text = %s | key = %s | encrypted_text = %s\n' % (
            str(self.plain_text), str(self.key), str(self.encrypted_text))

    def __str__(self):
        return self.__unicode__()


class CoincidenceHolder(object):
    def __init__(self, results):
        self.results = results
        self.coincidence_map = {}

    def check_coincidences(self):
        for result in self.results:
            if self.coincidence_map.has_key(result.encrypted_text):
                coincidence_amount = self.coincidence_map.get(result.encrypted_text)
                coincidence_amount += 1
                self.coincidence_map[result.encrypted_text] = coincidence_amount
            else:
                self.coincidence_map[result.encrypted_text] = 1


def run_for_lab():
    results = []
    plain_text = 0
    for key in range(0, 2 << 16 - 1):
        cipher = MiniPresent(key)
        encrypted_text = cipher.encrypt(plain_text)
        decrypted_text = cipher.decrypt(encrypted_text)
        result = ResultHolder(decrypted_text, key, encrypted_text)
        results.append(result)
        result_file.writelines(str(result))
    coincidence_holder = CoincidenceHolder(results)
    coincidence_holder.check_coincidences()
    result_map = {}
    for i in coincidence_holder.coincidence_map.values():
        if result_map.has_key(i):
            result_amount = result_map.get(i)
            result_amount += 1
            result_map[i] = result_amount
        else:
            result_map[i] = 1
    all_values_amount = 0
    line_chart = pygal.Line()
    line_chart.title = 'Coincidence chart'
    line_chart.x_title = 'Number of identical numbers'
    line_chart.y_title = 'Number of identical numbers sets'
    for key, value in result_map.items():
        if value == 1:
            result_file.writelines(("%d equal values were met %d time\n") % (key, value))
        else:
            result_file.writelines(("%d equal values were met %d times\n") % (key, value))
        all_values_amount += key * value
    line_chart.x_labels = map(str, result_map.keys())
    line_chart.add('coincidence', result_map.values())
    result_file.writelines(("all values amount = %d\n") % all_values_amount)
    line_chart.render_to_file('coincidence_chart.svg')
    return results, coincidence_holder, result_map


def test_all():
    key = 0x0
    plain_1 = 0
    plain_2 = "1"
    plain_3 = "2"
    result_file.writelines(str(plain_1))
    result_file.writelines(plain_2)
    result_file.writelines(plain_3)
    cipher = MiniPresent(key)
    encrypted_1 = cipher.encrypt(plain_1)
    encrypted_2 = cipher.encrypt(plain_2)
    encrypted_3 = cipher.encrypt(plain_3)
    enc_1 = encrypted_1
    enc_2 = encrypted_2.encode('hex')
    enc_3 = encrypted_3.encode('hex')
    result_file.writelines(str(enc_1))
    result_file.writelines(enc_2)
    result_file.writelines(enc_3)

    decrypted_1 = cipher.decrypt(encrypted_1)
    decrypted_2 = cipher.decrypt(encrypted_2)
    decrypted_3 = cipher.decrypt(encrypted_3)
    decr_1 = decrypted_1
    decr_2 = decrypted_2.encode('hex')
    decr_3 = decrypted_3.encode('hex')
    result_file.writelines(str(decr_1))
    result_file.writelines(decr_2.decode('hex'))
    result_file.writelines(decr_3.decode('hex'))

    results = run_for_lab()
    result_file.close()


if __name__ == "__main__":
    test_all()