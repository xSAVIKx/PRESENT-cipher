# coding=utf-8
import pygal

from present.miniPresent import MiniPresent

__author__ = 'Iurii Sergiichuk'

result_file = open('./results.txt', 'w+')


class EncryptedTextResultHolder(object):
    def __init__(self, encrypted_text):
        """
        :type encrypted_text str
        """
        self.encrypted_text = encrypted_text
        self.inversions_amount = self.check_inversions()

    def check_inversions(self):
        inversions_amount = 0
        textToCheck = self.encrypted_text
        lst = [int(i) for i in str(textToCheck)]
        for i in xrange(1, len(lst)):
            valueToCheck = lst[i]
            for j in xrange(0, i):
                value = lst[j]
                if valueToCheck < value:
                    inversions_amount += 1
        return inversions_amount


class ResultHolder(object):
    def __init__(self, plain_text, key, encrypted_text):
        self.plain_text = plain_text
        self.key = key
        self.encrypted_text = encrypted_text
        self.encrypted_text_holder = EncryptedTextResultHolder(encrypted_text)

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


def test_enc_all_open_texts():
    KEYS_MAX_LENGTH = 2 << 16 - 1
    OPEN_TEXTS_MAX_LENGTH = 2 << 8 - 1
    results = [[0 for col in xrange(0, OPEN_TEXTS_MAX_LENGTH + 1)] for row in xrange(0, OPEN_TEXTS_MAX_LENGTH + 1)]
    print "result len=%d" % len(results)
    print "result[0] len=%d" % len(results[0])
    for init in xrange(0, OPEN_TEXTS_MAX_LENGTH):
        results[init + 1][0] = init
        results[0][init + 1] = init
    results[0][0] = '#'
    print("init ended")
    for open_text in xrange(0, OPEN_TEXTS_MAX_LENGTH):
        for key in xrange(0, KEYS_MAX_LENGTH):
            cipher = MiniPresent(key)
            encrypted_text = cipher.encrypt(open_text)
            results[encrypted_text + 1][open_text + 1] += 1
    print("results received. writing to the file")
    with open('./all_texts.txt', 'w+') as all_texts_file:
        all_texts_file.write('\t\t\tOPEN TEXTS\n')
        for i in results:
            for j in i:
                all_texts_file.write('{0}'.format(str(j).rjust(5)))
            all_texts_file.write('\n')


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

    # TODO render inversion into svg chart
    return results, coincidence_holder, result_map


def test_all():
    key = 0x0
    plain_1 = 0
    plain_2 = 255
    plain_3 = 1025
    result_file.writelines(str(plain_1))
    result_file.writelines(str(plain_2))
    result_file.writelines(str(plain_3))
    cipher = MiniPresent(key)
    encrypted_1 = cipher.encrypt(plain_1)
    encrypted_2 = cipher.encrypt(plain_2)
    encrypted_3 = cipher.encrypt(plain_3)
    enc_1 = encrypted_1
    enc_2 = encrypted_2
    enc_3 = encrypted_3
    result_file.writelines(str(enc_1))
    result_file.writelines(str(enc_2))
    result_file.writelines(str(enc_3))

    decrypted_1 = cipher.decrypt(encrypted_1)
    decrypted_2 = cipher.decrypt(encrypted_2)
    decrypted_3 = cipher.decrypt(encrypted_3)
    decr_1 = decrypted_1
    decr_2 = decrypted_2
    decr_3 = decrypted_3
    result_file.writelines(str(decr_1))
    result_file.writelines(str(decr_2))
    result_file.writelines(str(decr_3))

    results = run_for_lab()
    result_file.close()


if __name__ == "__main__":
    test_all()
    test_enc_all_open_texts()
