#!/usr/bin/python
# _*_ coding: utf-8 _*_

import requests
import json
import pprint

get_json_to_dict = lambda url: dict(requests.get(url, headers={"content-type": "application/json"}).json().items())

filter_k = lambda func: lambda y: dict(filter(lambda x:func(x[0]), y.items()))
filter_v = lambda func: lambda y: dict(filter(lambda x:func(x[1]), y.items()))
filter_k_v = lambda func_k: lambda func_v: lambda x: filter_v(func_v)(filter_k(func_k)(x))

map_k = lambda func: lambda y: {k: v for k, v in zip(map(lambda x:func(x), y.keys()), y.values())}
map_v = lambda func: lambda y: {k: v for k, v in zip(y.keys(), map(lambda x:func(x), y.values()))}
map_k_v = lambda func_k: lambda func_v: lambda x: map_v(func_v)(map_k(func_k)(x))

filter_map_k_v = lambda f_k: lambda f_v: lambda m_k: lambda m_v: lambda x: map_k_v(m_k)(m_v)(filter_k_v(f_k)(f_v)(x))


if __name__ == "__main__":
	address_dict = get_json_to_dict("https://geolonia.github.io/japanese-addresses/api/ja.json")

	print("----------元の取得内容(市区町村は省略)----------")
	pprint.pprint(address_dict, depth=1)

	#関東に含まれるものはtrue
	is_kanto = lambda x: x in ['東京都', '神奈川県', '千葉県', '埼玉県', '茨城県', '栃木県', '群馬県']

	#市区長村が80件以上有ればtrue
	has_more_60 = lambda x: len(x) >= 60

	print("\n" + "----------関東のみ抽出(市区町村は省略)----------")
	pprint.pprint(filter_k(is_kanto)(address_dict), depth=1)

	print("\n" + "----------市区長村が60件以上ある県を抽出(市区町村は省略)----------")
	pprint.pprint(filter_v(has_more_60)(address_dict), depth=1)

	print("\n" + "----------関東、かつ市区長村が60件以上の県を抽出(市区町村は省略)----------")
	pprint.pprint(filter_k_v(is_kanto)(has_more_60)(address_dict), depth=1)

	#「都道府県」の文字列を削除
	trim_pref = lambda x: x if x[-1] == '道' else x[:-1]

	#「～町」のみ抽出
	get_town = lambda y: [s for s in y if s[-1] in ['町']]

	print("\n" + "----------「都道府県」の文字列を削除(市区町村は省略)----------")
	pprint.pprint(map_k(trim_pref)(address_dict), depth=1)

	print("\n" + "----------「～町」のみ抽出----------")
	pprint.pprint(map_v(get_town)(address_dict), depth=2)

	print("\n" + "----------「都道府県」の文字列を削除、かつ「～町」のみ抽出----------")
	pprint.pprint(map_k_v(trim_pref)(get_town)(address_dict), depth=2)

	print("\n" + "----------全部乗せ----------")
	pprint.pprint(map_k_v(trim_pref)(get_town)(address_dict), depth=2)