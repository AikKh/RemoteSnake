import pygame
import sys
import time
import random
from Snake import Snake
import socket, threading

class Board:

    blue = (50, 120, 213)
    green = (0, 255, 0)
    black = (0, 0, 0)
    red = (237, 41, 57)
    blood_red = (138, 3, 3)
    
    def __init__(self):
        self.snake = Snake((12, 12))
        
    def handle_messages(self, connection: socket.socket):
        
        while True:
            try:
                msg = connection.recv(1024)

                if msg:
                    if msg.decode() == 'LEFT':
                        self.snake._direction = 3
                    if msg.decode() == 'RIGHT':
                        self.snake._direction = 1
                    if msg.decode() == 'UP':
                        self.snake._direction = 0
                    if msg.decode() == 'DOWN':
                        self.snake._direction = 2
                else:
                    connection.close()
                    break

            except Exception as e:
                print(f'Error handling message from server: {e}')
                connection.close()
                break
        
    def appleGrownUp(self, surface):
        apple_x = random.randint(0, 24)
        apple_y = random.randint(0, 24)
        for snake_co in self.snake._cor:
            if snake_co == (apple_x, apple_y):
                return False
        pygame.draw.rect(surface, self.red, [apple_x  * 25, apple_y * 25, 25, 25])
        return (apple_x, apple_y)


    def snakeCutter(self, surface):
        for snake_co in self.snake._cor:
            pygame.draw.rect(surface, self.blue, [snake_co[0]  * 25, snake_co[1] * 25, 25, 25])
            

    def drawSnake(self, surface):
        for snake_co in self.snake._cor:
            pygame.draw.rect(surface, self.green, [snake_co[0]  * 25, snake_co[1] * 25, 25, 25])

    def limitCheck(self, head):
        if head[0] >= 25 or head[1] >= 25 or head[0] < 0 or head[1] < 0:
            return False
        return True

    def snakeDibilizmCheck(self, head):
        return head in self.snake._cor[1:]


    def game_over(self, surface):
        my_font = pygame.font.SysFont('times new roman', 49)
        game_over_surface = my_font.render('Game over man', True, self.blood_red)
        game_over_rect = game_over_surface.get_rect()
        game_over2_surface = my_font.render('Press 1 to try again or 0 to DIE', True, self.blood_red)
        game_over2_rect = game_over_surface.get_rect()
        score_surface = my_font.render('Score: {}'.format(len(self.snake._cor) - 1), True, self.blood_red)
        score_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (625/2, 625/4)
        game_over2_rect.midtop = (625/2 - 150, 625/4 + 160)
        score_rect.midtop = (625/2 + 70, 625/4 + 80)
        surface.fill(self.black)
        surface.blit(game_over_surface, game_over_rect)
        surface.blit(game_over2_surface, game_over2_rect)
        surface.blit(score_surface, score_rect)
        pygame.display.flip()
    

    def main(self):
        
        SERVER_ADDRESS = '127.0.0.1'
        SERVER_PORT = 1236
        
        socket_instance = socket.socket()
        socket_instance.connect((SERVER_ADDRESS, SERVER_PORT))
        
        threading.Thread(target=self.handle_messages, args=[socket_instance]).start()
        
        game_over = False
        last_choise = False

        speed = 0.1


        pygame.init()
        surface = pygame.display.set_mode((625, 625))
        surface.fill(self.blue)
        pygame.display.set_caption("Snake game")

        
        apple_cors = self.appleGrownUp(surface)

        while not game_over:

            while last_choise:
                self.game_over(surface)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.snake._head = (12, 12)
                            self.snake._direction = 0
                            self.snake._cor = [self.snake._cor[0]]
                            pygame.display.flip()
                            self.main()
                        elif event.key == pygame.K_0:
                            pygame.quit()
                            sys.exit()
            #time.sleep(0.1)
            time.sleep(speed)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.snake._direction == 1:
                            continue
                        print('LEFT')
                        socket_instance.send('LEFT'.encode())
                    elif event.key == pygame.K_RIGHT:
                        if self.snake._direction == 3:
                            continue
                        print('RIGHT')
                        socket_instance.send('RIGHT'.encode())
                    elif event.key == pygame.K_UP:
                        if self.snake._direction == 2:
                            continue
                        print('UP')
                        socket_instance.send('UP'.encode())
                    elif event.key == pygame.K_DOWN:
                        if self.snake._direction == 0:
                            continue
                        print('DOWN')
                        socket_instance.send('DOWN'.encode())

            self.snakeCutter(surface)
            self.snake.move()
            self.drawSnake(surface)

            if not self.limitCheck(self.snake._head) or self.snakeDibilizmCheck(self.snake._head):
                last_choise = True

            while not apple_cors:
                apple_cors = self.appleGrownUp(surface)

            if self.snake._head == apple_cors:
                speed = speed - speed/10
                pygame.draw.rect(surface, self.red, [apple_cors[0]  * 25, apple_cors[1] * 25, 25, 25])
                apple_cors = self.appleGrownUp(surface)
                self.snake.snakeMaker()
                
            pygame.display.flip()



game = Board()
game.main()


