#!/usr/bin/python
# _*_ coding: utf-8 _*_

import requests
import json
import collections

def get_json_to_list(url):
    return list(requests.get(url, headers={"content-type": "application/json"}).json())

def get_json_to_dict(url):
    return dict(requests.get(url, headers={"content-type": "application/json"}).json().items())

def filter_keys(func):
	return lambda y: dict(filter(lambda x:func(x[0]), y.items()))

def filter_values(func):
	return lambda y: dict(filter(lambda x:func(x[1]), y.items()))

def filter_key_val(f_key):
	return lambda f_value: lambda x: filter_values(f_value)(filter_keys(f_key)(x))

def map_keys(func):
	return lambda y: {k: v for k, v in zip(map(lambda x:func(x), y.keys()), y.values())}

def map_values(func):
	return lambda y: {k: v for k, v in zip(y.keys(), map(lambda x:func(x), y.values()))}

def map_key_val(f_key):
	return lambda f_value: lambda x: map_values(f_value)(map_keys(f_key)(x))

def filter_map_key_val(f_f_key):
	def f_value_map_key_val(f_f_value): 
		return lambda m_f_key: lambda m_f_value: lambda x: map_key_val(m_f_key)(m_f_value)(filter_key_val(f_f_key)(f_f_value)(x))
	return f_value_map_key_val

if __name__ == "__main__":
	url1 = "https://geolonia.github.io/japanese-addresses/api/ja.json"
	url2 = lambda pref, municipality: f'https://geolonia.github.io/japanese-addresses/api/ja/{pref}/{municipality}.json'

	is_kanto = lambda x: x in ['東京都', '神奈川県', '千葉県', '埼玉県', '茨城県', '栃木県', '群馬県']
	has_district = lambda x: len(x) > 50
	fill_string = lambda x: x.rjust(4,'＿')
	count_end_char = lambda x: dict(collections.Counter([s[-1] for s in x]))
	sort_municipality = lambda y: dict(sorted(count_end_char(y).items(), key=lambda x:['市', '区', '町', '村'].index(x[0])))

	#sort_municipality = lambda y: sorted(y, key=lambda x:['市', '区', '町', '村'].index(x[-1]))
	#filter_result = filter_key_val(is_kanto)(has_district)(get_json_to_dict(url))
	#map_result = map_key_val(fill_string)(sort_municipality)(filter_result)
	result = filter_map_key_val(is_kanto)(has_district)(fill_string)(sort_municipality)(get_json_to_dict(url1))
	for i in result.items():
		print(i)