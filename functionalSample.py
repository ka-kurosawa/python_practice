#!/usr/bin/python
# _*_ coding: utf-8 _*_

import requests
import json
import collections

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
	municipality_dict = get_json_to_dict("https://geolonia.github.io/japanese-addresses/api/ja.json")

	print('orginal_list:')
	for i in municipality_dict.items():
		print(i)

	is_kanto = lambda x: x in ['東京都', '神奈川県', '千葉県', '埼玉県', '茨城県', '栃木県', '群馬県']
	has_more_50 = lambda x: len(x) >= 50

	filter_result = filter_key_val(is_kanto)(has_more_50)(municipality_dict)
	print('filter_result:')
	for i in filter_result.items():
		print(i)

	fill_string = lambda x: x.rjust(4,'＿')
	sort_municipality = lambda y: dict(sorted(y, key=lambda x:['市', '区', '町', '村'].index(x[0])))
	count_end_char = lambda x: sort_municipality(collections.Counter([s[-1] for s in x]).items())


	map_result = map_key_val(fill_string)(count_end_char)(municipality_dict)
	print('map_result:')
	for i in map_result.items():
		print(i)

	filter_map_result = filter_map_key_val(is_kanto)(has_more_50)(fill_string)(count_end_char)(municipality_dict)
	print('filter_map_result:')
	for i in filter_map_result.items():
		print(i)