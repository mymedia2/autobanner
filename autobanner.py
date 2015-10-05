#!/usr/bin/env python3

import argparse
import random
import sys
import vk

TEXT_MESSAGE = "Поздравляем! Вы заняли {} место в нашем розыгрыше. Приз вам уже вручен."
CODICIL = "Если вы хотите отказаться от подарка, пишите https://vk.com/id147603034"
NUMERALS = [ "первое", "второе", "третье", "четвёртое", "пятое", "шестое", "седьмое", "восьмое", "девятое", "десятое" ]
PERIODS = [ 7 * 24 * 60 * 60, 24 * 60 * 60, 60 * 60 ]

POST_MESSAGE = """Итак, конкурс завершён. Список победителей определён, призы вручены.
Счастливчики:
{}
Кому не досталось бана, просьба не расстраиваться. Может, в следующий раз повезёт ;-)

Кому интересно, какими костылями пользовалась администрация, код на гитхабе https://github.com/mymedia2/autobanner
"""

def main():
	# 0_o

	arguments = get_args()
	participants = set(sys.stdin.read().split())
	number = 10 if len(participants) > 128 else 3
	winners = random.sample(participants, number)
	vkontakte = vk.API(access_token = arguments.access_token)
	current_time = vkontakte.getServerTime()
	reports = list()
	names = {
		u["id"]: " ".join([ u["first_name"], u["last_name"] ])
		for u in vkontakte.users.get(user_ids=",".join(winners))
	}

	for i, user in enumerate(winners):
		position = NUMERALS[i] if i < len(NUMERALS) else "{}-ое".format(i + 1)
		message = TEXT_MESSAGE.format(position)

		if i < len(PERIODS):
			expires = current_time + PERIODS[i]
		else:
			duration = random.randint(30 * 60, 365 * 24 * 60 * 60)
			if duration > 30 * 60 * 60:
				message += CODICIL
			expires = current_time + duration

		report = "{}. [id{}|{}]".format(i + 1, user, names[int(user)])
		if not arguments.simulate:
			try:
				vkontakte.groups.banUser(group_id=arguments.group_id, user_id=user,
										 end_date=expires, comment=message, comment_visible=1)
			except Exception as err:
				report += " ошибка, мы её обязательно исправим ({})".format(err)
		reports.append(report)

	text = POST_MESSAGE.format("\n".join(reports))
	print(text)
	if not arguments.simulate:
		post_id = vkontakte.wall.post(owner_id=-arguments.group_id, message=text)["post_id"]
		vkontakte.wall.pin(owner_id=-arguments.group_id, post_id=post_id)

def get_args(argv=sys.argv[1:]):
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("-s", "--simulate", action="store_true", help="Только вывести список победителей")
	parser.add_argument("access_token")
	parser.add_argument("group_id", type=int)
	return parser.parse_args(argv)

if __name__ == "__main__":
	main()
