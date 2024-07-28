
# Зададим базовое поле
fild =[
    [" ", "0", "1", "2"],
    ["0", "-", "-", "-"],
    ["1", "-", "-", "-"],
    ["2", "-", "-", "-"],
]
# показываем поле
def p_fild (x):
    for i in range (len(x)):
        print(*x[i])

def chek_win (list):
    for i in range(len(list)):
        # совпали строки
        if list[i].count("X") == len(list) - 1 or list[i].count("O") == len(list) - 1:
           return 1
        # столбцы
        #инициализация счетчиков
        sum_x, sum_0, sum_d1_x, sum_d1_0, sum_d2_x, sum_d2_0 = 0, 0, 0, 0, 0, 0

        for j in range(len(list)): # строки
            # стобцы
            # print("list[j][i]",list[j][i])
            if list[j][i] == "X":
                sum_x += 1
            # print("sum_x", sum_x)
            if list[j][i] == "O":
                sum_0 += 1
            # диаганаль 1
            if list[j][j] == "X":
                sum_d1_x += 1
            if list[j][j] == "O":
                sum_d1_0 += 1
            # диаганаль 2
            if j+1 <= len(list)-1: # обрабатываем смещение
                if list[len(list)-1-j][j+1] == "X":
                    sum_d2_x += 1
                elif list[len(list)-1-j][j+1] == "O":
                    sum_d2_0 += 1

        # подводим итоги после каждой строки
        if any([sum_x == len(list) - 1,
                sum_0 == len(list) - 1,
                sum_d1_x == len(list) -1,
                sum_d1_0 == len(list) -1,
                sum_d2_x == len(list) -1,
                sum_d2_0 == len(list) -1]):
                    return 1


#Получаем на вход значение, от игрока.
p_fild(fild)

sum_step = 1

while sum_step != 10: # ходов не может быть большe 10
    step = input(f"Ход {sum_step}, Укажите координаты шага, через пробел: ")# Получаем значение координат
    step_list = list(map(int,step.split()))

    #print(step_list)
    # Определяем символ, все нечетные это X все четные это 0
    if sum_step % 2:
        x_0 = "X"
    else:
        x_0 = "O"

    # Обновляем список
    fild[step_list[0]+1][step_list[1]+1] = x_0

    # выводим обновленное поле
    p_fild(fild)
    #chek_win(fild)
    #Проверяем победа или нет?
    if chek_win(fild):
        print("Ход был победным !!!")
        print(f"Победили {x_0}, на {sum_step} ходу")

        break
    sum_step += 1

