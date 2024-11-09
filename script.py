import argparse
import random

from django.db import models
from datacenter.models import Lesson, Schoolkid, Commendation, Mark, Chastisement

compliments = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2,
                                                         3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(child, subject):
    lessons = Lesson.objects.filter(year_of_study=child.year_of_study,
                                    group_letter=child.group_letter,
                                    subject__title=subject)
    lesson = lessons.order_by('date').last()
    if not lesson:
         return 'Урок не найден'
    Commendation.objects.get_or_create(teacher=lesson.teacher,
                                       subject=lesson.subject,
                                       created=lesson.date,
                                       schoolkid=child,
                                       text=random.choise(compliments))


def main():
    parser = argparse.ArgumentParser(
        description=
        'Этот скрипт используя имя и фамилию ученика позволяет изменять оценки в электронном дневнике, а так же удалять замечания ученика и заменять их на похвалу.'
    )
    parser.add_argument(
        '--name',
        type=str,
        help='Введите полное имя ученика. например: Алексей Романов')
    parser.add_argument('--subject',
                        type=str,
                        help='Введите название предмета. например: математика')
    args = parser.parse_args()
    try:
        child = Schoolkid.objects.get(full_name__contains=args.name)
    except Schoolkid.ObjectDoesNotExist:
        raise Schoolkid.ObjectDoesNotExist("Ученик с таким именем не найден") 
    except Schoolkid.MultipleObjectsReturned:
        raise Schoolkid.MultipleObjectsReturned("Найдено несколько учеников, уточните запрос!")
    fix_marks(child)
    remove_chastisements(child)
    create_commendation(child, args.subject)


if __name__ == '__main__':
    main()
