""" Програма-світлофор.
   Створити програму-емулятор світлофора для авто і пішоходів.
   Після запуска програми на екран виводиться в лівій половині -
   колір автомобільного, а в правій - пішохідного світлофора.
   Кожну секунду виводиться поточні кольори. Через декілька ітерацій -
   відбувається зміна кольорів - логіка така сама як і в звичайних
   світлофорах.
   Приблизний результат роботи наступний:
      Red        Green
      Red        Green
      Red        Green
      Red        Green
      Yellow     Green
      Yellow     Green
      Green      Red
      Green      Red
      Green      Red
      Green      Red
      Yellow     Red
      Yellow     Red
      Red        Green
"""

import time


def traffic_lights(duration):

    # When we have YELLOW after RED for traffic, we have GREEN for
    # pedestrians to finish their walk.
    # When we have YELLOW after GREEN for traffic, we have RED for
    # pedestrians because they should wait until traffic stops

    if duration < 5:
        print("More than 5")

    colour_traf = "Green"  # for traffic
    colour_ped = "Red"     # for pedestrians

    while True:
        i = 0
        while i < duration:
            print(colour_traf, colour_ped, sep="\t")
            time.sleep(1)
            i += 1
            if i == duration - 2:
                colour_traf = "Yellow"
        colour_traf = "Red" if colour_ped == "Red" else "Green"
        colour_ped = "Green" if colour_traf == "Red" else "Red"


duration = int(input("Duration of traffic greenlight, minimum 5 sec: "))
traffic_lights(duration)
