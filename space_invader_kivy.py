import random
import math
import os

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 1
BULLET_SPEED = 10
NUM_OF_ENEMIES = 2

class Player(Image):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.source = 'player.png'
        self.pos_hint = {'center_x': 0.5, 'y': 0}

    def move_left(self):
        if self.x > 0:
            self.x -= PLAYER_SPEED

    def move_right(self):
        if self.right < SCREEN_WIDTH:
            self.x += PLAYER_SPEED

    def fire_bullet(self):
        if self.parent and not self.parent.bullet.state == "fire":
            bullet = self.parent.bullet
            bullet.pos_hint = {'center_x': self.center_x, 'top': self.top}
            bullet.fire()

class Bullet(Image):
    state = "ready"

    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        self.source = 'bullet.png'
        self.state = "ready"
        self.pos_hint = {'center_x': 0.5, 'top': 1}

    def fire(self):
        self.state = "fire"
        self.parent.sound_laser.play()

    def move(self):
        if self.state == "fire":
            self.y += BULLET_SPEED
            if self.top > SCREEN_HEIGHT:
                self.state = "ready"

class Enemy(Image):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
        self.source = 'Alien1.png'
        self.pos_hint = {'center_x': random.random(), 'top': random.random()}

    def move(self):
        self.y -= ENEMY_SPEED

class Background(Image):
    def __init__(self, **kwargs):
        super(Background, self).__init__(**kwargs)
        self.source = 'Space1.jpg'
        self.allow_stretch = True

class SpaceInvaderGame(Widget):
    player = ObjectProperty(None)
    bullet = ObjectProperty(None)
    sound_laser = SoundLoader.load("laser.wav")
    sound_explosion = SoundLoader.load("explosion.wav")
    enemies = []

    def __init__(self, **kwargs):
        super(SpaceInvaderGame, self).__init__(**kwargs)
        self.background = Background()
        self.add_widget(self.background)
        self.player = Player()
        self.bullet = Bullet()
        self.add_widget(self.player)
        self.add_widget(self.bullet)
        for _ in range(NUM_OF_ENEMIES):
            enemy = Enemy()
            self.enemies.append(enemy)
            self.add_widget(enemy)

    def update(self, dt):
        self.player.move_left()
        self.player.move_right()
        self.bullet.move()
        for enemy in self.enemies:
            enemy.move()
            if enemy.y < 0:
                self.enemies.remove(enemy)
                self.remove_widget(enemy)
                new_enemy = Enemy()
                self.enemies.append(new_enemy)
                self.add_widget(new_enemy)

        for enemy in self.enemies:
            if self.bullet.collide_widget(enemy):
                self.enemies.remove(enemy)
                self.remove_widget(enemy)
                new_enemy = Enemy()
                self.enemies.append(new_enemy)
                self.add_widget(new_enemy)
                self.bullet.state = "ready"
                self.sound_explosion.play()
                break

        for enemy in self.enemies:
            if self.player.collide_widget(enemy):
                popup = Popup(title='Game Over',
                              content=BoxLayout(orientation='vertical', padding=10, spacing=10, children=[
                                  Label(text='GAME OVER'),
                                  Button(text='Quit', on_press=lambda *x: self.quit())
                              ]),
                              size_hint=(None, None), size=(400, 200))
                popup.open()
                self.player.pos_hint = {'center_x': 0.5, 'y': 0}
                self.bullet.pos_hint = {'center_x': 0.5, 'top': 1}
                for enemy in self.enemies:
                    self.remove_widget(enemy)
                self.enemies = []
                for _ in range(NUM_OF_ENEMIES):
                    enemy = Enemy()
                    self.enemies.append(enemy)
                    self.add_widget(enemy)
                break

    def quit(self):
        App.get_running_app().stop()

class SpaceInvaderApp(App):
    def build(self):
        game = SpaceInvaderGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    SpaceInvaderApp().run()
