
import pygame
import os
import random


# Создаём окно
pygame.init()
winW = 500
winH = 800
winSize = (winW, winH)
window = pygame.display.set_mode((winSize))

# Загружаем текстуры и задаём им нужный размер
# Текстура используемая для вертикального движения или состояния неподвижности
stationary_img = pygame.image.load(os.path.join("Textures", "Ship", "ship.png"))

# Массив из анимаций для поворота налево
left = [None]*5
for picIndexL in range(1,6):
    left[picIndexL-1] = pygame.image.load(os.path.join("Textures", "Ship","shipL" + str(picIndexL) + ".png" ))

# Массив из анимаций для поворота направо
right = [None]*5
for picIndexR in range(1,6):
    right[picIndexR-1] = pygame.image.load(os.path.join("Textures", "Ship","shipR" + str(picIndexR) + ".png" ))

# Текстура вражеских кораблей
enemy_img = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "ENEMY.png")), (50, 60))

# Текстура заднего фона
background_img = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "SPACE.png")), (winW, winH))

# Текстура пули
bullet_img = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "BULLETS", "bullet1.png")), (5, 15))

# Текстура базы
base_img = pygame.transform.scale(pygame.image.load(os.path.join("Textures", "Base.png")), (winW, 200))

#Создаём главный корабль
class Ship:
    """
    Класс Корабль это объект котрый управляется игроком.

    :param x: переменная, координата появления нашего объекта на оси X.
    :param y: переменная, координата появления нашего объекта на оси Y.

    Метод move_player отвечает за движение корабля.
    Метод draw отвечает за прорисовку корабля.
    Метод cooldown отвечает за задежку времени перед повторным выстрелом.
    Метод shoot отвечает за выстрел.
    Метод hit отвечает за попадание выстрела в противника.

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.step = 10
        self.move_right = False
        self.move_left = False
        self.standing = True
        self.stepIndex = 0

        self.bullets = []
        self.cool_down_count = 0

        self.lives = 3
        self.alive = True
        self.kills = 0

    # Движение
    def move_player(self, userInput):
        """
        Метод move_player отвечает за движение корабля.

        :param userInput: переменная, которая отслеживает какая клавиша нажата
        
        :return: None
        
        """
        # Проверка двигается ли корабль
        if userInput[pygame.K_DOWN] or userInput[pygame.K_UP] or userInput[pygame.K_RIGHT] or userInput[pygame.K_LEFT]:
            # Движение вниз
            if userInput[pygame.K_DOWN] and self.y <= winH-250:
                self.y += self.step
                self.move_right = False
                self.move_left = False
                self.standing = True
            # Движение вверх
            if userInput[pygame.K_UP] and self.y >= 0:
                self.y -= self.step
                self.move_right = False
                self.move_left = False
                self.standing = True

            # Движение вправо
            if userInput[pygame.K_RIGHT] and self.x <= winW-90:
                self.x += self.step
                self.move_right = True
                self.move_left = False
                self.standing = False

            # Движение влево
            if userInput[pygame.K_LEFT] and self.x >= 0:
                self.x -= self.step
                self.move_right = False
                self.move_left = True
                self.standing = False
    
        # Если стоим на месте
        else:
            self.move_right = False
            self.move_left = False
            self.standing = True
            self.stepIndex = 0
    
    # Прорисовка главного корабля в окне и его анимации поворота
    def draw(self, window):
        """
        Метод draw отвечает за прорисовку корабля.
        
        :param window: переменная, с областью на которой будет проходить прорисовка
        
        :return: None
        
        """

        # Анимация поворота влево
        if self.move_left:
            window.blit(left[self.stepIndex], (self.x, self.y))
            while self.stepIndex <= 3:
                self.stepIndex += 1
        
        # Анимация поворота вправо
        if self.move_right:
            window.blit(right[self.stepIndex], (self.x, self.y))
            while self.stepIndex <= 3:
                self.stepIndex += 1
        
        # Обычное состояние
        if self.standing:
            window.blit(stationary_img, (self.x, self.y))
    
    # Задержка для повторного выстрела
    def cooldown(self):
        """
        Метод cooldown отвечает за задежку времени перед повторным выстрелом.
        
        :param: None
        
        :return: None
        
        """
        if self.cool_down_count >= 10:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1    
    
    # Выстрел
    def shoot(self):
        """
        Метод shoot отвечает за выстрел.
        
        :param: None
        
        :return: None
        
        """
        self.hit()
        self.cooldown()
        if (userInput[pygame.K_SPACE] and self.cool_down_count == 0):
            bullet = Bullet1(self.x, self.y)
            self.bullets.append(bullet)
            bullet = Bullet2(self.x, self.y)
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move()
            if bullet.off_screen():
                self.bullets.remove(bullet)
    
    # Попадание в противника
    def hit(self):
        """
        Метод hit отвечает за попадание выстрела в противника.
        
        :param: None
        
        :return: None
        
        """
        for enemy in enemies:
            for bullet in self.bullets:
                if ((enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2]) and (enemy.hitbox[1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3])):
                    enemies.remove(enemy)
                    player.bullets.remove(bullet)
                    player.kills += 1

    

# Создаём пулю   
class Bullet1:
    """
    Класс Пуля1 это объект который вызывается при использовании метода shoot.
        
    :param x: переменная, координата появления нашего объекта на оси X.
    :param y: переменная, координата появления нашего объекта на оси Y.

    Метод draw_bullet отвечает за прорисовку пули.
    Метод move отвечает за движение пули.
    Метод off_screen отвечает за проверку выхода пули за пределы экрана.

    """

    def __init__(self, x, y):
        self.x = x + 15
        self.y = y + 20
    
    # Прорисовка 
    def draw_bullet(self, window):
        """
        Метод draw_bullet отвечает за прорисовку пули.

        :param window: переменная, с областью на которой будет проходить прорисовка.

        :return: None

        """
        window.blit(bullet_img, (self.x, self.y))
        
    # Движение
    def move(self):
        """
        Метод move отвечает за движение пули.
        
        :param: None

        :return: None

        """
        self.y -= 10
    
    # Проверка вышла ли пуля за пределы экрана
    def off_screen(self):
        """
        Метод off_screen отвечает за проверку выхода пули за пределы экрана.
        
        :param: None

        :return: None

        """
        return (self.y <= 0)


class Bullet2:
    """
    Класс Пуля2 это объект который вызывается при использовании метода shoot.
        
    :param x: переменная, координата появления нашего объекта на оси X.
    :param y: переменная, координата появления нашего объекта на оси Y.

    Метод draw_bullet отвечает за прорисовку пули.
    Метод move отвечает за движение пули.
    Метод off_screen отвечает за проверку выхода пули за пределы экрана.

    """
    def __init__(self, x, y):
        self.x = x + 65
        self.y = y + 20
    
    # Прорисовка 
    def draw_bullet(self, window):
        """
        Метод draw_bullet отвечает за прорисовку пули.

        :param window: переменная, с областью на которой будет проходить прорисовка.

        :return: None

        """
        window.blit(bullet_img, (self.x, self.y))
        
    # Движение
    def move(self):
        """
        Метод move отвечает за движение пули.
        
        :param: None

        :return: None

        """
        self.y -= 10
    
    # Проверка вышла ли пуля за пределы экрана
    def off_screen(self):
        """
        Метод off_screen отвечает за проверку выхода пули за пределы экрана.
        
        :param: None

        :return: None

        """
        return (self.y <= 0)


# Создаём корабли противников
class Enemy:
    """
    Класс Враг это объект который используется для вражеских кораблей.

    :param x: переменная, координата появления нашего объекта на оси X.
    :param y: переменная, координата появления нашего объекта на оси Y.
    :param speed: переменная, отвечающая за скорость движения вражеских кораблей.

    Метод draw_enemy отвечает за прорисовку противника.
    Метод move отвечает за движение противника.
    Метод off_screen отвечает за проверку косания вражеского корабля с базой.

    """
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.deaths = 0

        self.hitbox = (self.x, self.y + 10, 50, 45)

    # Прорисовка
    def draw_enemy(self, window):
        """
        Метод draw_enemy отвечает за прорисовку противника.

        :param window: переменная, с областью на которой будет проходить прорисовка.

        :return: None

        """

        window.blit(enemy_img, (self.x, self.y))
        self.hitbox = (self.x, self.y + 10, 50, 45)
    
    def move(self):
        """
        Метод move отвечает за движение противника.
        
        :param: None

        :return: None

        """
        self.y += self.speed
            

    def off_screen(self):
        """
        Метод off_screen отвечает за проверку косания вражеского корабля с базой.
        
        :param: None

        :return: None

        """
        return (self.y >= winH-100)

# Создаём задний фон
class Background:
    """
    Класс Задний фон это объект который используется для прорисовки и анимации заднего фона.

    :param x: переменная, координата появления нашего объекта на оси X.
    :param y: переменная, координата появления нашего объекта на оси Y.

    Метод draw_background отвечает за прорисовку и анимауию движения фона

    """
    def __init__(self, x, y):
        self.x = x
        self.y = y 
    
    # Прорисовка заднего фона и анимация движения
    def draw_background(self, window):
        """
        Метод draw_background отвечает за прорисовку и анимауию движения фона

        :param window: переменная, с областью на которой будет проходить прорисовка.

        :return: None

        """
        window.blit(background_img, (self.x, self.y))
        window.blit(background_img, (self.x, self.y-700))
        self.y += 1
        if self.y == 700:
            self.y = 0
            window.blit(background_img, (self.x, self.y ))            

# Прорисовываем элементы игры
def draw_game():
    """
    Функция draw_game отвечает за прорисовку текстур и остлеживание анимаций в игре.

    :param: None

    :return: None

     """
    global base_health, kills
    # Задний фон
    window.fill((0,0,0))
    bg.draw_background(window)
    
    #Главный корабль
    player.draw(window)
    
    #Пули
    for bullet in player.bullets:
        bullet.draw_bullet(window)

    # Противники 
    for enemy in enemies:
        enemy.draw_enemy(window)

    # База
    window.blit(base_img, (0, 630))
    
    # Проверка текущего состояния игрока, запуск экрана в случае смерти и перезапуск игры
    if player.alive == False:
        window.fill((0,0,0))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('You Died! Press R to restart', True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (winW // 2, winH // 2)
        window.blit(text, textRect)
        player.kills = -10
        if userInput[pygame.K_r]:
            player.alive = True
            base_health = 5
            player.kills = 0
    else:
        font = pygame.font.Font('freesansbold.ttf', 18)
        text_base_lives = font.render('Lives: '+ str(base_health), True, (255, 255, 255))
        text_kills = font.render('Kills: '+ str(player.kills), True, (255, 255, 255))
        window.blit(text_base_lives, (0, 0))
        window.blit(text_kills, (0, 15))

    
    # Частота кадров и обновление экрана
    pygame.time.delay(30)
    pygame.display.update()

# Задний фон
bg = Background(0, 0)
# Игрок
player = Ship(100, 100)
# Противники
enemies = []
# Счётчик убийств
kills = 0
# Счётчик жизней базы
base_health = 5




if __name__ == "__main__":
    runGame = True
    while runGame:
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runGame = False
                
        userInput = pygame.key.get_pressed()
        
        player.shoot()

        player.move_player(userInput)

        if base_health == 0:
            player.alive == False
        
        # Постепенное увелечение скорости и количества противников
        if len(enemies) < (player.kills + 10)//10:
            enemy = Enemy( random.randint(50, winW-50), -80, (player.kills + 10)//5)
            enemies.append(enemy)
        for enemy in enemies:
            enemy.move()
            if enemy.off_screen():
                enemies.remove(enemy)
                base_health -= 1
                if base_health <= 0:
                    player.alive = False


        draw_game()
    pygame.QUIT