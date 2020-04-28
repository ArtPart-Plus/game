import pygame
import random
import math

import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

##############
# 1. поставить задержку на дверях
# 2. накрутить звуки на все атаки
# 3. реализовать обучиение

##############

#анти задержка звука
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()
win = pygame.display.set_mode((500, 800))
pygame.display.set_caption("Легенды консоли beta 0.1")

#подгрузка изображений
bg = pygame.image.load('bg_1.png')
bg_fight = pygame.image.load('bg_Fight_1.png')
bg_lose = pygame.image.load('bg_lose_1.png')
bg_win = pygame.image.load('bg_win_1.png')
playerstand = pygame.image.load('start.png')
door = pygame.image.load('door.png')
lock = pygame.image.load('lock.png')
boss = pygame.image.load('boss_1.png')

archer_atk = pygame.image.load('archer_atk.png')
mage_atk = pygame.image.load('mage_atk.png')
witch_atk = pygame.image.load('witch_atk.png')
bone_atk = pygame.image.load('bone_atk.png')

#подгрузка музыки и звуков
pygame.mixer.music.load("game_1.wav")

sound_use = pygame.mixer.Sound("game_select.wav") 
sound_door = pygame.mixer.Sound("game_door.wav")
sound_fightstart = pygame.mixer.Sound("game_fightstart.wav")
sound_win = pygame.mixer.Sound("game_win.wav")
sound_lose = pygame.mixer.Sound("game_lose.wav")

#переменные для работы
clock = pygame.time.Clock()

#переменные персонажа
x = 235
y = 220
widht = 30
height = 50
speed = 5

fight_x = 75
fight_y = 310

#переменные врагов 
enemyAlive = True
enemy_x = 235
enemy_y = 220
enemy_widht = 30
enemy_height = 50

fight_enemy_x = 425 - enemy_widht
fight_enemy_y = 310

boss_x = 220
boss_y = 210
boss_widht = 60
boss_height = 80

#переменные дверей
doorlvl = 1
doorbosslvl = 10
doorLeft = True
doorUp = True
doorRight = True
doorDown = True
#
door_x_Left = 10
door_y_Left = 220
#
door_x_Up = 235
door_y_Up = 10
#
door_x_Right = 460
door_y_Right = 220
#
door_x_Down = 235
door_y_Down = 440
#
door_widht = 30
door_height = 50


#передвижение юнита
def moving():
    global x, y
    keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
    if keys [pygame.K_LEFT] and x > 10:
        x -= speed
    if keys [pygame.K_RIGHT] and x < 500 - widht - 10:
        x += speed
    if keys [pygame.K_UP] and y > 10:
        y -= speed
    if keys [pygame.K_DOWN] and y < 500 - height - 10:
        y += speed

#отрисовка окна
def drawWindow():
    win.blit(bg, (0, 0))
    #pygame.display.update()    (двойной апдейт миргание жопы)

#отрисовка персонажа
def drawHero():
    win.blit(playerstand, (x, y))

def drawHeroFight():
    win.blit(playerstand, (fight_x, fight_y))

#отрисовка врага
enemyAlive = False
def drawEnemy():
    if enemyAlive:
            win.blit(enemystand, (enemy_x, enemy_y))

def drawEnemyFight():
    if enemy.name == 'Босс':
        win.blit(enemystand, (fight_enemy_x, fight_enemy_y - 20))
    else:
        win.blit(enemystand, (fight_enemy_x, fight_enemy_y))

#отрисовка босса
def drawBoss():
    win.blit(boss, (boss_x, boss_y))

#отрисовка окна порожения 
def drawLose():
    win.blit(bg_lose, (0, 0))
    
i = 1    
def drawWin():
    global i
    win.blit(bg_win, (0, 0))
    if i == 1:
        pygame.mixer.music.load("game_win_end.wav")
        pygame.mixer.music.play(-1)
        i = 0 
        
    printText('Вы победили!!!', 20, 520)
    printText('Героя и врага я решил оставить здесь', 20, 540)
    printText('Автор кода Я. Музыки Я. Соло.', 20, 580)
    printText('Можно 5?', 20, 620)

#отрисовка дверей + логика
def drawDoor():
    global x, y, doorlvl, doorLeft, doorUp, doorRight, doorDown, enemyAlive, changeEnemy, boss_fight
    keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
        
    if doorLeft and fight == False:
        win.blit(door, (door_x_Left, door_y_Left))
        if enemyAlive:
            win.blit(lock, (door_x_Left, door_y_Left))
        else:
            if x + widht >= door_x_Left + 15 and x <= door_x_Left + door_widht - 15 and y + height >= door_y_Left + 20 and y <= door_y_Left + door_height - 20:
                printText('Войти в левую дверь?', 20, 540)
                printText(' |Y| Войти', 20, 580)
                if keys [pygame.K_y]:
                    if doorlvl + 1 >= doorbosslvl:
                        boss_fight = True
                        changeEnemy = 6
                        randomEnemy()
                        x = 460
                        y = 220 
                    else:
                        pygame.mixer.Sound.play(sound_door) #звук двери
                        #pygame.time.delay(400)
                        doorlvl += 1
                        print('Вошли в левую дверь. Уровень: ' + str(doorlvl)) #for log
                        print(' ') #for log
                        x = 460
                        y = 220
                        doorLeft = True
                        doorUp = True
                        doorRight = False
                        doorDown = True

                        enemyAlive = True
                        changeEnemy = random.randint(1,5) #выбор рандомного врага
                        randomEnemy() #инициализация врага
                        print(enemy.Lore) #for log
                

    if doorUp and fight == False:
        win.blit(door, (door_x_Up, door_y_Up))
        if enemyAlive:
            win.blit(lock, (door_x_Up, door_y_Up))
        else:
            if x + widht >= door_x_Up + 15 and x <= door_x_Up + door_widht - 15 and y + height >= door_y_Up + 20 and y <= door_y_Up + door_height - 20:
                printText('Войти в верхнюю дверь?', 20, 540)
                printText(' |Y| Войти', 20, 580)
                if keys [pygame.K_y]:
                    if doorlvl + 1 >= doorbosslvl:
                        boss_fight = True
                        changeEnemy = 6
                        randomEnemy()
                        x = 235
                        y = 440
                    else:
                        pygame.mixer.Sound.play(sound_door) #звук двери
                        #pygame.time.delay(400)
                        doorlvl += 1
                        print('Вошли в верхнюю дверь. Уровень: ' + str(doorlvl)) #for log
                        print(' ') #for log
                        x = 235
                        y = 440
                        doorLeft = True
                        doorUp = True
                        doorRight = True
                        doorDown = False

                    enemyAlive = True
                    changeEnemy = random.randint(1,5) #выбор рандомного врага
                    randomEnemy() #инициализация врага
                    print(enemy.Lore) #for log
                
                

    if doorRight and fight == False:
        win.blit(door, (door_x_Right, door_y_Right))
        if enemyAlive:
            win.blit(lock, (door_x_Right, door_y_Right))
        else:
            if x + widht >= door_x_Right + 15 and x <= door_x_Right + door_widht - 15 and y + height >= door_y_Right + 20 and y <= door_y_Right + door_height - 20:
                printText('Войти в правую дверь?', 20, 540)
                printText(' |Y| Войти', 20, 580)
                if keys [pygame.K_y]:
                    if doorlvl + 1 >= doorbosslvl:
                        boss_fight = True
                        changeEnemy = 6
                        randomEnemy()
                        x = 10
                        y = 220
                    else:
                        pygame.mixer.Sound.play(sound_door) #звук двери
                        #pygame.time.delay(400)
                        doorlvl += 1
                        print('Вошли в правую дверь. Уровень: ' + str(doorlvl)) #for log
                        print(' ') #for log
                        x = 10
                        y = 220
                        doorLeft = False
                        doorUp = True
                        doorRight = True
                        doorDown = True

                        enemyAlive = True
                        changeEnemy = random.randint(1,5) #выбор рандомного врага
                        randomEnemy() #инициализация врага
                        print(enemy.Lore) #for log
                

    if doorDown and fight == False:
        win.blit(door, (door_x_Down, door_y_Down))
        if enemyAlive:
            win.blit(lock, (door_x_Down, door_y_Down))
        else:
            if x + widht >= door_x_Down + 15 and x <= door_x_Down + door_widht - 15 and y + height >= door_y_Down + 20 and y <= door_y_Down + door_height - 20:
                printText('Войти в нижнюю дверь?', 20, 540)
                printText(' |Y| Войти', 20, 580)
                if keys [pygame.K_y]:
                    if doorlvl + 1 >= doorbosslvl:
                        boss_fight = True
                        changeEnemy = 6
                        randomEnemy()
                        x = 235
                        y = 10
                    else:
                        pygame.mixer.Sound.play(sound_door) #звук двери
                        #pygame.time.delay(400)
                        doorlvl += 1
                        print('Вошли в нижнюю дверь. Уровень: ' + str(doorlvl)) #for log
                        print(' ') #for log
                
                        x = 235
                        y = 10
                        doorLeft = True
                        doorUp = False
                        doorRight = True
                        doorDown = True

                        enemyAlive = True
                        changeEnemy = random.randint(1,5) # выбор рандомного врага
                        randomEnemy() # инициализация врага
                        print(enemy.Lore) #for log


    if fight == False and enemyAlive == True: 
        drawEnemy()#отрисовка врага


#котакт с врагом
def enemyContact():
    global fight
    keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш 

    if enemyAlive == True and fight == False:
        if x + widht >= enemy_x + 5 and x <= enemy_x + enemy_widht - 25 and y + height >= enemy_y + 20 and y <= enemy_y + enemy_height - 20:
            enemy.attribute() # печать атрибутов врага
            if keys [pygame.K_a]:
                pygame.mixer.Sound.play(sound_fightstart) #звук начала битвы
                fight = True



firstAtk = 0
printAtkInfo1 = 'Битва началась'
printAtkInfo2 = ' '
#битва с врагами 
def drawFight():
    global lose_screen, firstAtk, hero, enemyAlive, fight, fightEndInfo, onetick, printAtkInfo1, printAtkInfo2

    keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш

    win.blit(bg_fight, (0, 0)) #фон битвы
    printFightHP() #печать хп на сердечках

    if hero.hp <= 0:
        print('Вы проиграли')  #for log
        pygame.mixer.Sound.play(sound_lose) # звук проигрыша
        firstAtk = 0
        fight = False
        lose_screen = True
    elif enemy.hp <= 0:
        if enemy.name == 'Босс':
            drawWin()
        else:
            print('Вы победили')  #for log
            pygame.mixer.Sound.play(sound_win) # звук победы
            firstAtk = 0
            enemyAlive = False
            fight = False
            fightEndInfo = True
            onetick = True
    else:
        if firstAtk == 0:
            print ('Битва началась:')  #for log
            if hero.rangeAtk == enemy.rangeAtk:
                firstAtk = random.randint(1,2)
                if firstAtk == 1:
                    print('Герой атакует первый')  #for log
                else:
                    print('Враг атакует первый')  #for log
            elif hero.rangeAtk > enemy.rangeAtk:
                print('Герой атакует первый')  #for log
                firstAtk = 1
            else:
                print('Враг атакует первый')  #for log
                firstAtk = 2

            print(' ') #for log

        printText(' Press space to continue...', 20, 700)
        printText(printAtkInfo1, 20, 520)
        printText(printAtkInfo2, 20, 540)

        if firstAtk == 1:
            printText('Герой готовится совершить удар', 20, 580)
        else: 
            printText('Враг готовится совершить удар', 20, 580)
        
        if keys [pygame.K_SPACE]:
            
            #рандом урона
            heroRaundDmg = random.randint(hero.minDamage, hero.maxDamage)
            enemyRaundDmg = random.randint(enemy.minDamage, enemy.maxDamage)

            if firstAtk == 1:
                if heroRaundDmg == hero.minDamage:
                    print('Герой промахнулся') #for log
                    printAtkInfo1 = 'Герой промахнулся'
                    animAtk()
                elif heroRaundDmg == hero.maxDamage:
                    print('Герой критует') #for log
                    print('Герой наносит: ' + str(heroRaundDmg)) #for log
                    printAtkInfo1 = 'Герой критует'
                    printAtkInfo2 = 'Герой наносит: ' + str(heroRaundDmg) + ' единиц урона'
                    animAtk()  
                    enemy.hp = enemy.hp - heroRaundDmg
                    
                else:
                    print('Герой наносит: ' + str(heroRaundDmg)) #for log
                    printAtkInfo1 = 'Герой наносит: ' + str(heroRaundDmg) + ' единиц урона'
                    animAtk()  
                    enemy.hp = enemy.hp - heroRaundDmg
                    
                    


            if firstAtk == 2:
                if enemyRaundDmg == enemy.minDamage:
                    print('Враг промахнулся') #for log
                    printAtkInfo1 = 'Враг промахнулся'
                    animAtk()
                elif enemyRaundDmg == enemy.maxDamage:
                    print('Враг критует') #for log
                    print('Враг наносит: ' + str(enemyRaundDmg)) #for log
                    printAtkInfo1 = 'Враг критует'
                    printAtkInfo2 = 'Враг наносит: ' + str(enemyRaundDmg) + ' единиц урона'
                    animAtk()  
                    hero.hp = hero.hp - enemyRaundDmg
                    
                else:
                    print('Враг наносит: ' + str(enemyRaundDmg)) #for log
                    printAtkInfo1 = 'Враг наносит: ' + str(enemyRaundDmg) + ' единиц урона'
                    animAtk()  
                    hero.hp = hero.hp - enemyRaundDmg
                    
                    
            if firstAtk == 1:
                firstAtk = 2
            elif firstAtk == 2:
                firstAtk = 1
            print(' ') #for log
        
#анимация атаки
def animAtk():
    global hero, enemy, firstAtk, fight_enemy_x, fight_enemy_y, fight_x, fight_y

    animPlayAtk = True
    animPlayBack = True

    if firstAtk == 1:
        while animPlayAtk:
            clock.tick(100)
            win.blit(bg_fight, (0, 0)) #фон битвы
            printFightHP() #печать хп на сердечках

            if hero.Lore == 'Волшебника':
                win.blit(playerstand, (75, 310))
                win.blit(mage_atk, (fight_x + 10, fight_y))
            elif hero.Lore == 'Лучника':
                win.blit(playerstand, (75, 310))
                win.blit(archer_atk, (fight_x + 10, fight_y - 10))
            else:
                drawHeroFight()

            drawEnemyFight()

            fight_x = fight_x + speed
            
            if fight_x >= fight_enemy_x - widht:
                if hero.Lore == 'Волшебника' or hero.Lore == 'Лучника' :
                    fight_x = 75
                    animPlayAtk = False
                else:
                    while animPlayBack:
                        clock.tick(100)
                        win.blit(bg_fight, (0, 0)) #фон битвы
                        printFightHP() #печать хп на сердечках

                        drawHeroFight()
                        drawEnemyFight()

                        fight_x = fight_x - speed
                        if fight_x == 75:
                            animPlayAtk = False
                            animPlayBack = False

                        pygame.display.update()

            pygame.display.update()

    if firstAtk == 2:
        while animPlayAtk:
            clock.tick(100)
            win.blit(bg_fight, (0, 0)) #фон битвы
            printFightHP() #печать хп на сердечках

            drawHeroFight()

            if enemy.name == 'Ведьма':
                win.blit(enemystand, (425 - enemy_widht, 310))
                win.blit(witch_atk, (fight_enemy_x , fight_enemy_y))
            elif enemy.name == 'Скелет':
                win.blit(enemystand, (425 - enemy_widht, 310))
                win.blit(bone_atk, (fight_enemy_x , fight_enemy_y))
            else:
                drawEnemyFight()

            fight_enemy_x = fight_enemy_x - speed

            if fight_enemy_x <= fight_x + widht:
                if enemy.name == 'Ведьма' or enemy.name == 'Скелет':
                    fight_enemy_x = 425 - enemy_widht
                    animPlayAtk = False
                else:
                    while animPlayBack:
                        clock.tick(100)
                        win.blit(bg_fight, (0, 0)) #фон битвы
                        printFightHP() #печать хп на сердечках

                        drawHeroFight()
                        drawEnemyFight()

                        fight_enemy_x = fight_enemy_x + speed
                        if fight_enemy_x == 425 - enemy_widht:
                            animPlayAtk = False
                            animPlayBack = False

                        pygame.display.update()
                    
            pygame.display.update()    


#получение опыта  
def lvlup():
    global hero, lvlupinput, plusnewregen
    hero.xp += 1 
    print ('Герой получает 1 единицу опыта') #for log
    if hero.xp == hero.xpNewlvl:
        hero.lvl += 1
        lvlupinput = True
        hero.xp = 0
        hero.xpNewlvl = hero.xpNewlvl * 2

        #увеличение регенирации в 1.5 раз и округление до целого
        plusnewregen = round(hero.regen * 1.5)
        hero.regen = plusnewregen

        hero.minDamage = hero.minDamage + 2 #увеличение минимального урона героя на 2
        hero.maxDamage = hero.maxDamage + 2 #увеличение максимального урона героя на 2
        hero.hp += 5 #бонусные 5 hp

        #for log
        print(heroname + ' получает уровень ' + str(hero.lvl))
        print(' Герой получает бонусные 5 hp')
        print(' Урон героя увеличен на 2 единицы')
        print(' Регенерация здровья увеличена до ' + str(plusnewregen) + ' единиц')
        
    print('Герой отрегенерировал ' + str(hero.regen) + ' hp') #for log
    print(' ') #for log

#печать текста
def printText(message, x, y, font_color = (23, 19, 13), font_type = 'pixel.otf', font_size = 16):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    #pygame.display.update()    (двойной апдейт миргание жопы)

#печать текста (шрифт для хп)
def printTextBigWhite(message, x, y, font_color = (255, 255, 255), font_type = 'pixel.otf', font_size = 25):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    #pygame.display.update()    (двойной апдейт миргание жопы)

#печать текста (шрифт для лвл)
def printTextBigBlack(message, x, y, font_color = (0, 0, 0), font_type = 'pixel.otf', font_size = 25):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    win.blit(text, (x, y))
    #pygame.display.update()    (двойной апдейт миргание жопы)


#печать классов
def printCharacters():
    printText('[ Классы ]', 20, 520)
    printText(' |1| Лучник', 20, 540) 
    printText(' |2| Копьеносец', 20, 560) 
    printText(' |3| Чародей', 20, 580)
    printText(' |4| Рыцарь', 20, 600)
    printText(' |5| Целитель', 20, 620)

#печать HP + lvl + XP
def printLifestyle():
    printTextBigBlack(str(hero.hp), 29, 748)
    printTextBigWhite(str(hero.hp), 27, 750)
    printTextBigBlack(str(hero.lvl), 97, 746)
    printTextBigWhite(str(hero.lvl), 95, 748)
    printText(str(hero.xp) + "/" + str(hero.xpNewlvl), 122, 768)

#вывод хп в бою
def printFightHP():
	printTextBigBlack(str(hero.hp), 29, 119)
	printTextBigWhite(str(hero.hp), 27, 121)
	printTextBigBlack(str(enemy.hp), 454, 119)
	printTextBigWhite(str(enemy.hp), 452, 121)




class Playerclass():
    """Player unit"""

    def __init__ (self, name, Lore, hp, regen, rangeAtk, maxDamage, minDamage, lvl, xp, xpNewlvl):
        """Инициализация атрибутов героя"""
        self.name = name
        self.Lore = Lore
        self.hp = hp
        self.regen = regen
        self.rangeAtk = rangeAtk
        self.maxDamage = maxDamage
        self.minDamage = minDamage
        self.lvl = lvl
        self.xp = xp
        self.xpNewlvl = xpNewlvl

    def attribute(self):
        """Вывод атрибутов героя"""
        printText('Имя: ' + hero.name, 20, 520)
        printText('HP: ' + str(hero.hp), 20, 540)
        printText('Регенерация за ход: ' + str(hero.regen), 20, 560)

        if hero.rangeAtk == 1:
            printText('Тип атаки: дальний бой', 20, 580)
        else:
            printText('Тип атаки: ближний бой', 20, 580)

        avgdamage = (hero.minDamage + hero.maxDamage)/2
        printText('Средний урон: ' + str(avgdamage), 20, 600)
        printText(' Press space to continue...', 20, 700)

def pickCharacter(): 
    global playerstand, change, hero
    keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
    if keys [pygame.K_1]:
        pygame.mixer.Sound.play(sound_use) #звук использования
        hero = Playerclass(heroname, 'Лучника', 60, 2, 1, 10, 5, 1, 0, 2)
        playerstand = pygame.image.load('archer_idle.png')
        print('Выбрали ' + hero.Lore) #for log
        change = False
    if keys [pygame.K_2]:
        pygame.mixer.Sound.play(sound_use) #звук использования
        hero = Playerclass(heroname, 'Копьеносеца', 75, 3, 0, 12, 2, 1, 0, 2)
        playerstand = pygame.image.load('lancer_idle.png')
        print('Выбрали ' + hero.Lore) #for log
        change = False
    if keys [pygame.K_3]:
        pygame.mixer.Sound.play(sound_use) #звук использования
        hero = Playerclass(heroname, 'Волшебника', 45, 2, 1, 15, 6, 1, 0, 2)
        playerstand = pygame.image.load('mage_idle.png')
        print('Выбрали ' + hero.Lore) #for log
        change = False
    if keys [pygame.K_4]:
        pygame.mixer.Sound.play(sound_use) #звук использования
        hero = Playerclass(heroname, 'Рыцаря', 85, 4, 0, 7, 5, 1, 0, 2)
        playerstand = pygame.image.load('knight_idle.png')
        print('Выбрали ' + hero.Lore) #for log
        change = False
    if keys [pygame.K_5]:
        pygame.mixer.Sound.play(sound_use) #звук использования
        hero = Playerclass(heroname, 'Целителя', 65, 4, 0, 6, 3, 1, 0, 2)
        playerstand = pygame.image.load('priest_idle.png')
        print('Выбрали ' + hero.Lore) #for log
        change = False


class Enemyclass():
    """Enemy unit"""

    def __init__ (self, name, Lore, hp, rangeAtk, maxDamage, minDamage):
        """Инициализация атрибутов врага"""
        self.name = name
        self.Lore = Lore
        self.hp = hp
        self.rangeAtk = rangeAtk
        self.maxDamage = maxDamage
        self.minDamage = minDamage

    def attribute(self):
        """Вывод атрибутов врага""" 
        printText('Перед вами ' + enemy.name, 20, 540)
        printText('HP: ' + str(enemy.hp), 20, 560)

        if enemy.rangeAtk == 1:
            printText('Тип атаки: дальний бой', 20, 580)
        else:
            printText('Тип атаки: ближний бой', 20, 580)

        enemy_avgdamage = (enemy.minDamage + enemy.maxDamage)/2
        printText('Средний урон: ' + str(enemy_avgdamage), 20, 600)
        printText(' |A| Начать бой', 20, 640)


#рандомный враг из списка
changeEnemy = 0
def randomEnemy():
    global changeEnemy, enemy, enemystand, enemyAlive
    if changeEnemy == 1:
        enemy = Enemyclass('Волк', 'Спавн волка', 20, 0, 5, 1)
        enemystand = pygame.image.load('wolf_idle.png')

    if changeEnemy == 2:
        enemy = Enemyclass('Динозавр', 'Спавн динозавра', 24, 0, 6, 4)
        enemystand = pygame.image.load('rex_idle.png')

    if changeEnemy == 3:
        enemy = Enemyclass('Ведьма', 'Спавн ведьмы', 18, 1, 8, 4)
        enemystand = pygame.image.load('witch_idle.png')

    if changeEnemy == 4:
        enemy = Enemyclass('Энт', 'Спавн энта', 26, 0, 4, 2)
        enemystand = pygame.image.load('ent_idle.png')

    if changeEnemy == 5:
        enemy = Enemyclass('Скелет', 'Спавн скелета', 10, 1, 10, 8)
        enemystand = pygame.image.load('bone_idle.png')

    if changeEnemy == 6:
        enemy = Enemyclass('Босс', 'Спавн босса', 35, 0, 12, 8)
        enemystand = pygame.image.load('boss_1.png')
    
    

            

        
 




#!-------------------------------------------------------------------------------------


#ввод имени персонажа с консоли
heroname = str(input('Введите имя персонажа: '))


#цикл игры
music = True
rungame = True
lose_screen = False
change = True
change_1 = True
fight = False
fightEndInfo = False
lvlupinput = False
boss_fight = False
while rungame:
    
    clock.tick(30)
    drawWindow()
    drawDoor()
    drawHero()

    #выход через крестик
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
    
    
    #бесконечный цикл музыки
    while music:
        pygame.mixer.music.play(-1)
        music = False
    

    # -> инициализация выбора персонажа
    while change:
        clock.tick(30)
        drawWindow()
        win.blit(playerstand, (x, y))
        
        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                change = False
        
        
        printCharacters() #вывод персонажей
        pickCharacter()

        pygame.display.update()
    
    # -> вывод выбора персонажа
    while change_1:
        clock.tick(30)
        drawWindow()
        drawHero()
        
        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                change_1 = False
        
        

        hero.attribute()

        #выход с цикла на пробел
        keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
        if keys [pygame.K_SPACE]:
            pygame.mixer.Sound.play(sound_use) #звук использования
            change_1 = False

        printLifestyle()
        moving()

        pygame.display.update()

    
    # -> вывод боя
    soundFight = True
    while fight:
        clock.tick(30)
        # работа с музыкой
        if soundFight == True:
            pygame.mixer.music.load("game_fight_1.wav")
            pygame.mixer.music.play(-1)
            soundFight = False




        drawFight() #отрисовка битвы
        drawHeroFight() #отрисовка героя в битве
        drawEnemyFight() #отрисовка врага в битве



        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                fight = False

        # работа с музыкой
        if fight == False:
            pygame.mixer.music.load("game_1.wav")
            pygame.mixer.music.play(-1)
        
        pygame.display.update()

    # -> вывод инфы после битвы
    while fightEndInfo:
        clock.tick(30)
        drawWindow()
        drawHero()

        #отрисовка дверей
        if doorLeft:
            win.blit(door, (door_x_Left, door_y_Left))
        if doorUp:
            win.blit(door, (door_x_Up, door_y_Up))
        if doorRight:
            win.blit(door, (door_x_Right, door_y_Right))
        if doorDown:
            win.blit(door, (door_x_Down, door_y_Down))
        
        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                fightEndInfo = False

        #выход с цикла на пробел
        keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
        if keys [pygame.K_SPACE]:
            pygame.mixer.Sound.play(sound_use) #звук использования
            fightEndInfo = False
            lvlupinput = False

        while onetick:
            printAtkInfo1 = 'Битва началась'
            printAtkInfo2 = ' '
            lvlup()
            hero.hp += hero.regen
            onetick = False
        
        #выводить инфу о изменениях в герое
        printText('Вы победили!', 20, 520)
        printText(' Герой получает 1  единицу опыта', 20, 540) 
        printText(' Герой отрегенерировал ' + str(hero.regen) + ' hp', 20, 560)
        if lvlupinput == True:
            printText(heroname + ' получает уровень ' + str(hero.lvl), 20, 600)
            printText(' Герой получает бонусные 5 hp', 20, 620)
            printText(' Урон героя увеличен на 2 единицы', 20, 640)
            printText(' Регенерация здровья увеличена до ' + str(plusnewregen) + ' единиц', 20, 660)
    

        printText(' Press space to continue...', 20, 700)

        printLifestyle()
        

        pygame.display.update()

    # -> вывод экрана поражения
    soundLose = True
    while lose_screen: 
        clock.tick(30)

        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                lose_screen = False

        drawLose()
        printText('Ты проиграл     o_o', 20, 520)
        printText('Но не переживай я с тобой =) ', 20, 540)

        printText('P.S:', 20, 580)
        printText('Рестарта не будет))))))))))', 20, 600)
        printText('Перезапускай игру сам)))', 20, 620)
        # работа с музыкой
        if soundLose == True:
            pygame.mixer.music.load("game_lose_screen.wav")
            pygame.mixer.music.play(-1)
            soundLose = False

        pygame.display.update()

    # -> битва с боссом
    while boss_fight:
        clock.tick(30)
        drawWindow()
        drawBoss()
        drawHero()
        keys = pygame.key.get_pressed() #переменная проверки зажатия клавиш
        
        #выход через крестик
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rungame = False
                boss_fight = False

        if x + widht >= boss_x + 5 and x <= boss_x + boss_widht - 25 and y + height >= boss_y + 20 and y <= boss_y + boss_height - 20:
            enemy.attribute() # печать атрибутов врага
            if keys [pygame.K_a]:
                pygame.mixer.Sound.play(sound_fightstart) #звук начала битвы
                fight = True
                boss_fight = False
        
        
        printLifestyle()
        moving()

        pygame.display.update()




    
    enemyContact()                                                                                                
    printLifestyle()
    moving()
    
    printText('Добро пожаловать в игру "Легенда Консоли"! ', 20, 520)
    
    pygame.display.update()
    

pygame.quit()