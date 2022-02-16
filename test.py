
def task_d():
    print("Задание d: ")
    a = float(input("Введите a=: "))
    b = float(input("Введите b=: "))

    result = (3*a**3 - 2*a*b + b**2)/(2*a*(3*a-b))
    print("Результат: ", result)

task_d()
