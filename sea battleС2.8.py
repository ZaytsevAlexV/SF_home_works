
import random as rnd

#класс позиции элемента, хранящий значения х и у
class Pos:
    def __init__(self,x,y) ->None:
        self.x = x
        self.y = y

    def __eq__(self, other):
       return self.x == other.x and self.y == other.y

# класс карабля, порождаем его из базового класса фигуры
class Ship:
    def __init__(self,x, y, way, len_ship): # way - направление H - горизонтальное,  V- вертикальное.
        self.x = x # начальная координата (строка)
        self.y = y # начальная координата (столбец)
        self.way = way  # way - направление H - горизонтальное,  V- вертикальное.
        self.len_ship = len_ship

    # метод получения координат коробля
    def get_coord_lst_ship(self) -> list:
        list_coord = []
        if self.way == "H":
            for i in range(self.len_ship):  # сбор координат каждой палубы корабля и запсить в список
                list_coord.append(Pos(self.x, (self.y + i)))
        elif self.way == "V":
            for j in range(self.len_ship):  # сбор координат каждой палубы корабля и запить в список
                list_coord.append(Pos((self.x + j), (self.y)))
        return list_coord


class BoardGame:
    def __init__(self, size_field):
        self.__size_field = size_field
        self.__shot_list = []  # список выстрелов
        #self.ship_list = []  # список короблей пользователя
        self.__ship_coord = []  # список координат короблей пользователя
        self.__damaged_list = []  # список координат повреждений караблей
        self.__fild_to_render = [] # список, хранить общий слой состояния игрового поля

    # изменяем лог доску под список изменений, актуальное поле
    def setBoardRender(self,coord_chang,type=""):
        if type == "start":
            self.__fild_to_render = coord_chang
        else:
            for p in coord_chang:
                if type == "coord_ship":
                    self.__fild_to_render[p.x][p.y] = "■"
                elif type == "coord_shot" and self.__fild_to_render[p.x][p.y] == "■":
                    self.__fild_to_render[p.x][p.y] = "X"
                else:
                    self.__fild_to_render[p.x][p.y] = "Т"

    #запоминаем координаты карабля на доске
    def setShipOnBoard(self,ship_coord):
        for s in ship_coord:
            self.__ship_coord.append(s)
        self.setBoardRender(ship_coord,"coord_ship")

    # запоминаем координаты выстрела
    def setShot(self,shot):
        _lst = []
        self.__shot_list.append(shot)
        _lst.append(shot)
        self.setBoardRender(_lst,"coord_shot")

    def getFild_to_render(self):
        return self.__fild_to_render

    def getShipCoord(self):
        return self.__ship_coord

    def getSizeBoard(self):
        return self.__size_field
    # метод проверки на въождение в список
    def chek_pos_in_list(self,pos, list):
        for i in list:
            #print(f"list_shot{i.x},{i.y}.{type(pos)}")
            #print(f"Pos{pos.x},{pos.y}.{type(pos)}")
            if pos == i: # перегрузили равенство у класса, поэтому должно стработать
                return  i # если есть в списке, тогда выводим что есть и выходим.
                break
        return None

    def getShotList(self):
        return self.__shot_list
    def delShipCoord(self,pos):
        self.__ship_coord.remove(pos)

    def setDamadgedList(self,pos):
        self.__damaged_list.append(pos)


class LogicSeaBattle:
    #логика создания базового поля
    def get_start_boad(self,board)->None:
        lst_start_board = [["0"]*board.getSizeBoard() for i in range(board.getSizeBoard()) ]
        board.setBoardRender(lst_start_board,"start")

    # логика добавление карабля на поле
    def add_ship(self,pos,w,type,board)-> None:
        #создаем объект
        ship = Ship(pos.x,pos.y,w,type)
        #проверяем попадают ли все координаты в граници поля
        for coord_ship in ship.get_coord_lst_ship():
            #print(f"пробегаем по координатам корабля{coord_ship.x,coord_ship.y}")
            if any([coord_ship.x < 0,
                    coord_ship.y < 0,
                    coord_ship.x > board.getSizeBoard()-1,
                    coord_ship.y > board.getSizeBoard()-1
                    ]):
                print("корабль выходит за граници поля")
                raise ValueError(f"Введите повторно ")

        #проверяем есть ли рядом корабли на доске
        if self.chek_ship_near(ship.get_coord_lst_ship(),board.getShipCoord()):
            #print("Рядом нет кораблей")
            board.setShipOnBoard(ship.get_coord_lst_ship())
        else:
            print("Рядом есть корабли")
            raise ValueError (f"Введите повторно ")
            #добавляю на доску координаты корабля

        #print(f"{pos.x},{pos.y},{w},{type}")
        #print(f"{ship.x},{ship.y},{ship.way},{ship.len_ship}")

    def add_shot(self,shot,board):
        #проверяем был ли ранее такой выстре в доске
        if board.chek_pos_in_list(shot,board.getShotList()):
            print("ранее уже был такой выстрел сделан")
            raise ValueError(f"Введите повторно ")
        board.setShot(shot)
        #print(f"выстрел добавлен в список {shot} в {board.getShotList()}")

        #проверяем было ли попадение, и если было мы исключаем тогда координату коробля с поля
        index_coord=board.chek_pos_in_list(shot, board.getShipCoord())
        #print(f"результат проверки на вхождение в список {index_coord}")
        if index_coord:
            board.delShipCoord(index_coord)
            board.setDamadgedList(shot)

    def chek_win(self,board) ->bool:
        if board.getShipCoord():
            #print("-- Игра продолжается --")
            return False
        else:
            return True


    def chek_ship_near(self, ship_coord, list_coord_ship) -> bool: #True - проверку прошел, false - проверку не прошел
        for p in ship_coord:
            for p_list_ship in list_coord_ship:
                # print(f"{p.x},{p.y}")
                # print(p_list_ship)
                #print(f"{p_list_ship.x}{p_list_ship.y}")
                if any([p == Pos(p_list_ship.x - 1, p_list_ship.y - 1),
                        p == Pos(p_list_ship.x - 1, p_list_ship.y),
                        p == Pos(p_list_ship.x - 1, p_list_ship.y + 1),
                        p == Pos(p_list_ship.x, p_list_ship.y - 1),
                        p == Pos(p_list_ship.x, p_list_ship.y + 1),
                        p == Pos(p_list_ship.x + 1, p_list_ship.y + 1),
                        p == Pos(p_list_ship.x + 1, p_list_ship.y),
                        p == Pos(p_list_ship.x + 1, p_list_ship.y + 1)]):
                    return False  # проверку не прошел
                    break
        return True

    #создаем карабли компьютера
    def addCompShip(self,list_ship_type,board)->None:
        for ship_type in list_ship_type:
           list_way = ["H","V"]
           ok = True
           while ok:
               try:
                   # добавляем карабль на докуску
                   self.add_ship(Pos(rnd.randint(0,board.getSizeBoard()-1),rnd.randint(0,board.getSizeBoard()-1)),rnd.choice(list_way),ship_type,board)
               except ValueError:
                   ok = True
               else:
                   ok = False

    #Добавляем выстрел компютера на доску Игрока
    def addShotComp(self, user_board) -> None:
        ok = True
        while ok:
            try:
                self.add_shot(Pos(rnd.randint(0,user_board.getSizeBoard()-1),rnd.randint(0,user_board.getSizeBoard()-1)),user_board)
            except ValueError:
                ok = True
            else:
                ok = False

class GUIConsol:
    def __init__(self,size_fild, list_type_ships)->None:
        self.__size_fild = size_fild
        self.__list_type_ships = list_type_ships
        self.logic = LogicSeaBattle() # Объект логики
        self.__comp_board = BoardGame(size_fild) # объект поля компьютера
        self.__user_board = BoardGame(size_fild) # объект поля игрока

    # метод выводит поле на экран логическую доску
    def show(self, board):
        print()
        print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i, row in enumerate(board):
            row_str = f" {i + 1} | {' | '.join(row)} |"  # формируем строки, как в крестиках ноликах
            print(row_str)
        print()

    #отвечает только за сбор информации о корабле
    def init_ship(self, type):
        ok = True
        while ok:
            try:
                x = int(input(
                    f"Введите координаты {type} палубного коробля, X: ")) - 1  # уменьшаем порядок на один, т.к. пользователь видет другое
                if 0>x or x>self.__size_fild-1:
                    print(f"Значение в X выходит за границу поля")
                    raise ValueError(f"Введите правильное значение")
                y = int(input(
                    f"Введите координаты {type} палубного коробля, Y: ")) - 1  # уменьшаем порядок на один, т.к. пользователь видет другое
                if 0>y or y>self.__size_fild-1:
                    print(f"Значение в Y выходит за границу поля")
                    raise ValueError(f"Введите правильное значение")
                if type != 1:
                    w = input("Введите направление (H - горизонтально, V - ветикально):")
                    w = str.upper(w)
                    if w != "H" and w !="V":
                        print(f"Некорректно указано направление корабля {w}, а должно быть H или V")
                        raise ValueError (f"Введите правильное значение")
                else:
                    w = "H"
            except ValueError:
                    ok = True
                    print ("Неверное значение при вводе данных корабля")
            else:
                #print("все хорошо")
                ok = False
                return Pos(x,y), w, type
                break

    # основной графический метот он же отвечает за запуск
    def run(self):
        # старт
        # создаем базовую доску через логику
        self.logic.get_start_boad(self.__user_board)
        self.logic.get_start_boad(self.__comp_board)

        # показываем текущее состояние доски пользователя
        self.show(self.__user_board.getFild_to_render())

        # Установка караблей пользователем
        for ship_type in self.__list_type_ships:
            ok = True
            while ok:
                try:
                    #создаем карабль. В GUI мы собираем данные и передаем в логику на добавление карабля, на доску пользователя
                    self.logic.add_ship(*self.init_ship(ship_type), self.__user_board) #тут разварачиваем атрибуты
                except ValueError:
                    print(f"Введите еще раз корабль")
                else:
                    print(f"Корабль установлен!")
                    ok = False
                    #показываем поле с караблем
                    self.show(self.__user_board.getFild_to_render())

        # логика по созданию караблей компа
        self.logic.addCompShip(self.__list_type_ships,self.__comp_board)

        # выводим поле компа
        print("##### Поле компа #####")
        self.show(self.__comp_board.getFild_to_render())
        print("######################")

        # Запрашиваем выстрелы
        while True:
            print("введите координаты выстрела")
            ok = True
            while ok:
                try:
                    # запаршиваем выстрелы
                    shot_x = int(input(" Строка, X: ")) - 1
                    if 0 > shot_x or shot_x > self.__size_fild-1:
                       print(f"Значение в X выходит за границу поля")
                       raise ValueError(f"Введите правильное значение")

                    shot_y = int(input(" Столбец, Y: ")) - 1
                    if 0 > shot_y or shot_y > self.__size_fild-1:
                       print(f"Значение в Y выходит за границу поля")
                       raise ValueError(f"Введите правильное значение")

                    #отправляем в логику выстрела на доску компьютера
                    self.logic.add_shot(Pos(shot_x, shot_y), self.__comp_board)
                except ValueError:
                    print(f" Повторите ввод координат: ")
                else:
                    ok = False

                    # отправляем в логику выстрел компьютера
                    self.logic.addShotComp(self.__user_board)

                    print("###### Ваша достка ######")
                    self.show(self.__user_board.getFild_to_render())#Показываем доску

                    print("###### Доска компьютера ######")
                    self.show(self.__comp_board.getFild_to_render())  # Показываем доску

            if self.logic.chek_win(self.__comp_board):
               print("**********************  Поздравляем. Вы победили!!! **********************")
               break

            if self.logic.chek_win(self.__user_board):
               print(" КОНЕЦ. Сожелеем, компьютер победил (((")
               break

#запус программы
if __name__ == "__main__":
    # базовые переменные
    lst_type_ship = [3, 2, 1, 1]  # список типов короблей.
    f = 6 # ширина / высота поля
    game = GUIConsol(f,lst_type_ship)
    game.run()


