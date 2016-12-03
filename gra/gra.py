#!/usr/bin/env python

import math
import pygame
from pygame.locals import *
from random import randint

#kolorki:
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (0xBF,0x0F,0xB5)
	                       
S, W = 900, 600

#kafelki
class Brick(pygame.sprite.Sprite):

   width = 59
   height = 33
   def __init__(self, img, x, y, score):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface( (self.width, self.height) )
      self.image = pygame.image.load(img).convert()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.score = score

   def update(self, bonus, x, y):
      self.gdyBonus(bonus, x, y)

   def gdyBonus(self, bonus, x, y):
      addbonus = randint(0, 25)
      if addbonus == 0:
         type = randint(0, 3)
         bon = Bonus(x, y, type)
         bonus.add(bon)

#bonusy
class Bonus(pygame.sprite.Sprite):
  def __init__(self, x, y, type):
     pygame.sprite.Sprite.__init__(self)
     self.x = x
     self.y = y
     self.size = 30
     self.type = type
     pygame.sprite.Sprite.__init__(self)
     self.image = pygame.Surface((self.size, self.size))
     self.image = pygame.image.load(bonus).convert()
     self.rect = self.image.get_rect()
     self.rect.centerx = self.x
     self.rect.centery = self.y

  def update(self):
     self.y += 10
     self.x += 0
     self.rect.centerx = self.x
     self.rect.centery = self.y


#pilka
class Ball(pygame.sprite.Sprite):

    speed = 12.0
    direction = 50 
    size = 12

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = pos
        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, purple, (5,5), 5 )
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def bounce(self,diff):
        self.direction = ((180 - self.direction) % 360)
        self.direction -= diff

    def update(self):

        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x - 5
        self.rect.y = self.y

        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        if self.x > S - self.size:
            self.direction = (360 - self.direction) % 360
            self.x = S - self.size - 1

#pad
class Pad(pygame.sprite.Sprite):

  max_width = 120
  max_height = 10

  def __init__(self, pad_width, pad_height):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((pad_width, pad_height))
      self.image.fill((purple))
      self.rect = self.image.get_rect()
      self.rect.topleft = (0, W - pad_height)


  def update(self, screen, invisibility, p_pos, pad_width):
      self.rect.left = p_pos - pad_width/2
      self.image = pygame.Surface( (pad_width, 10) )
      self.image.fill(purple)
      if self.rect.left < 0:
         self.rect.left = 0
      if self.rect.right > S:
         self.rect.right = S
      if not invisibility:
         screen.blit(self.image, (self.rect.left,self.rect.top) )

#stan gry
class StanGry():
   score = 0
   lives = 5
   extraTime = 80
   sukces, porazka = False, False
   pad_centerx = S / 2
   moving = False

#ustawienia
bricks = ["bricks/niebieski.PNG", "bricks/zielony.PNG", "bricks/czerwony.PNG", "bricks/zolty.PNG", "bricks/rozowy.PNG"]
bonus = "bonus/bonus.png"

brick_width, brick_height = 59, 33
pad_width, pad_height = 80, 10

pad_centerx = S / 2

done = True
notstarted = True
collision = False
extraTime = 30

gamestate = StanGry()

#funkcje
def usun(G):
   for s in G.sprites():
      if s.y < 0 or s.y > W:
         G.remove(s)

def clear(G):
   for s in G.sprites():
      G.remove(s)

def resetujBonusy():
   global bonusTime, bonusStates, bonuses
   bonusStates = [False, False, False, False]
   bonusTime = [0, 0, 0, 0]
   clear(bonuses)

def SprawdzWarunkiGry():

   if gamestate.lives < 1:
      gamestate.porazka = True
      sound_porazka.play()
   if len(blocks) == 0:
      gamestate.sukces = True
      sound_sukces.play()
   if ball.y > W:
      gamestate.lives -= 1
      gamestate.moving = False
      resetujBonusy()

def aktualizujPunkty():
   if notstarted:
      font_surface = font.render("PUNKTY: " + str(gamestate.score) + "             ZYCIA: " + str(gamestate.lives), False, purple)
      screen.blit(font_surface, (205,5))
   if gamestate.porazka:
      text = font.render("You are loser!", True, white)
      textpos = text.get_rect(centerx = background.get_width()/2)
      textpos.top = 300
      screen.blit(text, textpos)
   if gamestate.sukces:
      text = font.render("Gratki, Mistrzu!", True, white)
      textpos = text.get_rect(centerx = background.get_width()/2)
      textpos.top = 300
      screen.blit(text, textpos)

def rysuj():
   blocks.draw(screen)
   bonuses.draw(screen)
   balls.draw(screen)

def odliczanie(wait):
   if wait > 0:
      wait -= 1
   return wait




#tlo
pygame.init()
screen = pygame.display.set_mode([S, W])
background = pygame.Surface(screen.get_size())
pygame.mouse.set_visible(0)

font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 20)
zegar = pygame.time.Clock()

#dzwieki
pygame.mixer.init()
sound_start = pygame.mixer.Sound("sounds/start.wav")
sound_sukces = pygame.mixer.Sound("sounds/aplauz.wav")
sound_porazka = pygame.mixer.Sound("sounds/loser.wav")
sound_zbicie = pygame.mixer.Sound("sounds/zbicie.wav")
sound_padOdbicie = pygame.mixer.Sound("sounds/pad.wav")
sound_bonus = pygame.mixer.Sound("sounds/dzwoneczek.wav")

balls = pygame.sprite.Group()
paddles = pygame.sprite.Group()

#tu ma być taki wektor?
bonusStates = [False , False , False , False]
bonusTime = [0,0,0,0]

bonuses = pygame.sprite.Group()
blocks = pygame.sprite.Group()

large_pad = Pad(120, 10)
small_pad = Pad(40, 10)
normal_pad = Pad(80, 10)

pad = large_pad

ball = Ball((pad_centerx, 590))

#wall
def rysujWalla():
   top = 85
   left = 90
   global blocks
   for i in range(6):
       for j in range(12):
            block = Brick(bricks[(2*(j+i)+i^3) % 3], left + j * (brick_width + 3), top, 20)
            blocks.add(block)
       top += brick_height + 5
   for j in range(12):
            block = Brick(bricks[3], left + j * (brick_width + 3), top, 30)
            blocks.add(block)

rysujWalla()
sound_start.play()

#loop
while done:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = False
      if event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            done = False
         if event.key == K_SPACE:
            gamestate.moving = True
         if event.key == K_r:
            gamestate = StanGry()
            pad_centerx = S / 2
            resetujBonusy()
            clear(balls)
            blocks.empty()
            rysujWalla()
            sound_start.play()

   
   screen.fill(black)
   pressed = pygame.key.get_pressed()

   if pressed[K_LEFT]:
      pad_centerx -= 15
   if pressed[K_RIGHT]:
      pad_centerx += 15
   if pad_centerx > S:
      pad_centerx = S - pad_width / 2
   if pad_centerx < 0:
      pad_centerx = pad_width / 2
   aktualizujPunkty()

   if not gamestate.porazka and not gamestate.sukces:

      if gamestate.moving == False:
         balls.remove(ball)
         ball = Ball((pad_centerx, 590))
         balls.add(ball)
         ball.bounce(130)

      if bonusStates[0]:
         pad_width = 40
         pad= small_pad
      if bonusStates[1]:
         pad_width = 100
         pad = large_pad
      if not bonusStates[0] and not bonusStates[1]:
         pad_width = 70
         pad = normal_pad
      pad.update(screen, bonusStates[2], pad_centerx, pad_width)

      balls.update()

      if pygame.sprite.spritecollide(pad, balls, False):
         diff = (pad.rect.left + pad_width / 2) - (ball.rect.left + ball.size / 2)
         ball.rect.top = W - pad_height - ball.size
         ball.bounce(diff)
         sound_padOdbicie.play()

      tobeRemoved = [];
      
      for b in balls:
         for block in blocks:
            if(pygame.sprite.collide_rect(b,block)):
                  block.update(bonuses, b.x, b.y)
                  tobeRemoved.append(block)
                  gamestate.score += block.score
                  sound_zbicie.play()
                  if not bonusStates[3]:
                      b.bounce(0)

      for r in tobeRemoved:
          r.kill();

      for b in bonuses:
          if (pygame.sprite.collide_rect(pad, b)):
             bonusStates[b.type] = True
             bonusTime[b.type] += extraTime
          sound_bonus.play()

      bonuses.update()

      for i in range(0,3):
         if(bonusTime[i] > 0):
             bonusTime[i] -= 1
         if(bonusTime[i] == 0):
            bonusStates[i] = False

      rysuj()

      zegar.tick(30)

      usun(balls)
      usun(bonuses)

      SprawdzWarunkiGry()

   pygame.display.update()

pygame.display.quit()
pygame.font.quit()
exit()
