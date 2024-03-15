import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

exit_shedule = []
def validate_date(date):
    try:
        day, month, year = map(int, date.split(':'))
        formatted_date = f'{year}-{month:02d}-{day:02d}'
        return formatted_date
    except ValueError:
        return None

while True:
    date = input("Введите дату(число:месяц:год) : ")
    formatted_date = validate_date(date)
    if formatted_date:
        break
    else:
        print("Некорректный формат даты. Пожалуйста, введите дату в формате 'число:месяц:год'.")


name = input("Введите имя преподавателя : ")
request = requests.get(f'https://ruz.spbstu.ru/search/teacher?q={name}')
soup = BeautifulSoup(request.text, "lxml")

a_tags = soup.find_all("a", class_="search-result__link")

teachers_info = []
lessons_counter = [0, 0, 0, 0, 0, 0]
pattern_teacher_id = r'/teachers/(\d+)">(.*?)</a>'

for a_tag in a_tags:    
    match = re.search(pattern_teacher_id, str(a_tag))
    if match:
        teacher_id = match.group(1)
        teacher_name = match.group(2)
        teachers_info.append({"id": teacher_id, "name": teacher_name})



for i, teacher_info in enumerate(teachers_info):
    print(f"{i+1}. {teacher_info['name']} (id: {teacher_info['id']})")

choice = int(input("Выберите номер преподавателя: "))
print()
print()

if 1 <= choice <= len(teachers_info):
    #f = open("html2.txt", "w")
    selected_teacher = teachers_info[choice - 1]
    teacher_id = selected_teacher['id']
    req_teach = requests.get(f"https://ruz.spbstu.ru/teachers/{teacher_id}?date={formatted_date}")
    if req_teach.ok:
        second_soup = BeautifulSoup(req_teach.text, "lxml")
        schedule = second_soup.findAll('li', class_='schedule__day')
        cur_day = ''
        for day in schedule:
            print(day.find(class_='schedule__date').text, '\n------------------------')
            cur_day = day.find(class_='schedule__date').text
            if(cur_day[(len(cur_day)-2):len(cur_day)] == 'пн'):i = 0
            elif(cur_day[(len(cur_day)-2):len(cur_day)] == 'вт'):i = 1
            elif(cur_day[(len(cur_day)-2):len(cur_day)] == 'ср'):i = 2
            elif(cur_day[(len(cur_day)-2):len(cur_day)] == 'чт'):i = 3
            elif(cur_day[(len(cur_day)-2):len(cur_day)] == 'пт'):i = 4
            elif(cur_day[(len(cur_day)-2):len(cur_day)] == 'сб'):i = 5  
            for lesson in day.findAll(class_='lesson'):
                print(lesson.find(class_='lesson__subject').text)
                print(lesson.find(class_='lesson__type').text)
                if str(lesson).find('href="/faculty/') != -1:
                    a = lesson.find(class_='lesson__groups').text
                    if 'Поток' in a:
                        res1 = a[28:]
                        res2 = ', '.join([res1[i:i+7] + res1[i+7:i+13] for i in range(0, len(res1), 13)])
                        res = 'Группы: ' + res2
                    else:
                        res = a[15:]
                    print(res)
                print(lesson.find(class_='lesson__places').text)
                print()
                if i < len(lessons_counter):
                    lessons_counter[i] += 1
        

        days_per_week = ['Понедельник', 'Вторник', 'Среда ', 'Четверг ', 'Пятница', 'Суббота']
        lessons_per_day = lessons_counter
        
        plt.bar(days_per_week, lessons_per_day)
        plt.title('Статистика')
        plt.xlabel('День недели')
        plt.ylabel('Количество занятий')

        plt.savefig("output", dpi = 1000, facecolor='y',edgecolor = 'w',
                     bbox_inches="tight", pad_inches=0.1, transparent=True)
        plt.show()
    else:
        print(f"Ошибка при выполнении запроса: {req_teach.status_code}")
else:
    print("Некорректный выбор.")
