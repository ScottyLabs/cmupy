#!/usr/bin/env python

import re
import urllib
import urllib2

from bs4 import BeautifulSoup

def valid_andrew_id(andrewid):
    # regex written by Jacob Zimmerman
    return type(andrewid) is str and re.match(r'^[a-zA-Z][a-zA-Z0-9]{1,7}$', andrewid) is not None

class Directory:
    base_url = 'http://directory.andrew.cmu.edu'
    directory_uri = '/search/basic/results'

    @classmethod
    def search(cls, query):
        data = urllib.urlencode({ 'search[generic_search_terms]': query })
        req = urllib2.Request(cls.base_url + cls.directory_uri, data)
        return BeautifulSoup(urllib2.urlopen(req).fp)

    @classmethod
    def get_info(cls, query=None, andrewid=None):
        '''
        Given a query, returns a list of all the people who match
        that query. Given a valid Andrew ID, returns the person with
        that Andrew ID.

        '''
        def parse_person_soup(soup):
            # this function name is more terrifying than I intended
            if soup.find(id='no_results_error'):
                return None

            results = soup.find(id='search_results')
            if 'people matched your search criteria' in results.h1.get_text():
                raise ValueError('Not a directory page: %s' % results.h1.get_text())

            sections = results.find_all(class_='directory_section')
            def parse_info_line(info_line):
                key = info_line.find_all(class_='directory_field')[0].get_text().strip()
                key = key[:len(key)-1] # strip out colon
                value = info_line.get_text().split(':')[1].strip()
                return (key, value)
            data = []
            for section in sections:
                lines = section.find_all('div')
                if len(lines) == 1:
                    data.append(parse_info_line(section))
                else:
                    data += [parse_info_line(info_line) for info_line in lines]
            return dict(data)
        if andrewid is not None:
            if not valid_andrew_id(andrewid):
                raise ValueError('Given Andrew ID is not valid.')
            soup = cls.search(andrewid)
            results = soup.find(id='search_results')
            if 'people matched your search criteria' in results.h1.get_text():
                raise ValueError('Not a unique Andrew ID: %s' % results.h1.get_text())
            return parse_person_soup(cls.search(andrewid))
        elif query is not None:
            soup = cls.search(query)
            if soup.find(id='no_results_error'):
                return []
            results = soup.find(id='search_results')
            column_labels = [th.find_all('div')[-1].get_text().strip() for th in results.find_all('tr')[0].find_all('th')]
            people = results.find_all('tr')[1:]
            people_data = []
            for person in people:
                person_data = [td.get_text().strip() for td in person.find_all('td')]
                people_data.append(dict(zip(column_labels, person_data)))
            return people_data
        else:
            return ValueError('Must provide either a search query or a valid Andrew ID.')

if __name__ == '__main__':
    print("Results of 'tom' query: \n%s" % str(Directory.get_info('tom')))
    print("zhixians's info: \n%s" % str(Directory.get_info(andrewid='zhixians')))