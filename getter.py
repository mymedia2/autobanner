#!/usr/bin/env python3

"""Печатает идентификаторы записей-репостов заданной записи

Использование: ./getter.py access_token post_id

Все идентификаторы записей имеют формат 123_456 ,
где 123 – id владельца (для групп отрицательный),
    456 – id записи на стене владельца.
"""

import collections
import sys
import vk

def main():
	arguments = get_args()
	vkontakte = vk.API(access_token = arguments.access_token)
	owner_id, post_id = arguments.post_id.split("_")
	result = vkontakte.wall.getReposts(owner_id=owner_id, post_id=post_id, count=1000)
	for post in result["items"]:
		print("{}_{}".format(post["from_id"], post["id"]))

def get_args(argv=sys.argv[1:]):
	"""Парсит аргументы и возвращает именованный кортеж с аргументами.

	Имитирует работу библиотеки argparse. При использованиии оригинальной
	бибилотеки возникает проблема обработки id группы.
	"""
	if len(argv) == 1 and argv[0] in { "--help", "-h" }:
		print(__doc__, file=sys.stderr)
		sys.exit()

	if len(argv) != 2:
		print("Неверные аргументы", file=sys.stderr)
		sys.exit(1)

	Arguments = collections.namedtuple("Arguments", ["access_token", "post_id"])
	return Arguments(argv[0], argv[1])

if __name__ == "__main__":
	main()
