#!/usr/bin/env python

import copy
import urllib2
import unicodedata

from bs4 import BeautifulSoup

class PrinterStatus:
    def __init__(self):
        status_url = 'https://clusters.andrew.cmu.edu/printerstats/'
        req = urllib2.Request(status_url)
        handler = urllib2.urlopen(req)
        if handler.getcode() != 200:
            raise Exception('Unable to retrive printer status from %s' % status_url)

        soup = BeautifulSoup(handler.fp)
        data_table = soup.find_all(class_='epi-dataTable')[0]
        rows = data_table.find_all('tr')
        status_data = {}
        def parse_header_row(row):
            data = []
            for th in row.find_all('th'):
                text = th.get_text().strip()
                if text == u'':
                    data.append(u'Usable?')
                else:
                    data.append(text.replace(u'\xa0', u' '))
            return data

        data_labels = parse_header_row(rows[0])[1:]

        def parse_row(row):
            if len(row.td.find_all('td')) == 0:
                data = []
                for td in row.find_all('td'):
                    try:
                        text = td.img['src'].split('.')[0]
                    except:
                        text = td.get_text().replace(u'\xa0', u' ').strip()
                    data.append(text.lower())
                return data
            else:
                # their HTML is malformed
                data = []
                for child in row.td.contents:
                    if child is not None and len(child.strip()) != 0:
                        data.append(child.strip().replace(u';', u''))
                        break
                for td in row.td.find_all('td'):
                    try:
                        text = td.img['src'].split('.')[0]
                    except:
                        text = td.get_text().replace(u'\xa0', u' ').strip()
                    data.append(text.lower())
                return data

        for row in rows[1:]:
            data = parse_row(row)
            status_data[data[0]] = dict(zip(data_labels, data[1:]))

        self.raw_status = status_data
        self.status = {}
        def u2a(text):
            '''Normalizes unicode and converts to ascii'''
            return unicodedata.normalize('NFKD', text).encode('ascii','ignore')
        for printer_name, raw_printer_status in self.raw_status.items():
            printer_status = {}
            try:
                usable = raw_printer_status[u'Usable?']
                if usable == u'go':
                    printer_status['status'] = 'ready'
                elif usable == u'yield':
                    printer_status['status'] = 'caution'
                else:
                    printer_status['status'] = 'not ready'
                printer_status['details'] = u2a(raw_printer_status[u'LCD Message'])
            except:
                printer_status = {
                    'status': None,
                    'details': 'No printer status data found.'
                }
            self.status[u2a(printer_name).strip().lower()] = printer_status

    def get_status(self, name):
        query_toks = name.lower().strip().split()
        for printer_name, printer_status in self.status.items():
            if set(query_toks).issubset(printer_name.split()):
                return printer_status
        return None

    def get_all_statuses(self):
        return copy.deepcopy(self.status)

if __name__ == '__main__':
    ps = PrinterStatus()
    print('Status of Gates 3 printer:\n%s' % str(ps.get_status('Gates 3')))