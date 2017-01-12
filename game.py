import sys
import pygame as pg

CAPTION = "Bweakowt"
SCREEN_SIZE = [640, 480]


class Ball(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        super(Ball, self).__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = [0.0, 0.0]
        self.velocity = [0.0, 0.0]


class Scene(object):
    def __init__(self):
        pass

    def update(self, screen):
        raise NotImplementedError

    def render(self, screen):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class LevelScene(Scene):
    def __init__(self, level):
        super(LevelScene, self).__init__()
        self.level = level
        self.ball = Ball(pg.Color("green"), 5, 5)
        self.ball.pos = [pg.mouse.get_pos()[0], 380]
        self.states = ["PRE", "LIVE", "WIN", "LOSE"]
        self.state = self.states[0]
        self.paddle_width = 100
        self.paddle = pg.Rect(pg.mouse.get_pos()[0] - 50, 400, self.paddle_width, 10)

    def update(self, screen):
        if self.state == self.states[0]:
            self.paddle.x = pg.mouse.get_pos()[0] - 50
            self.ball.pos = [pg.mouse.get_pos()[0], 380]
        elif self.state == self.states[1]:
            if self.ball.velocity == [0.0, 0.0]:
                pass # just clicked, set random velocity/slope?
            else:
                pass # check for collisions, bounce around, etc.

    def render(self, screen):
        screen.fill(pg.Color("black"))
        screen.blit(self.ball.image, self.ball.pos)
        screen.fill(pg.Color("red"), self.paddle)

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif e.type == pg.MOUSEBUTTONDOWN and self.state == self.states[0]:
                self.state = self.states[1]


class TitleScene(Scene):
    def __init__(self):
        super(TitleScene, self).__init__()
        self.title_font = pg.font.SysFont("Arial", 56)
        self.subtitle_font = pg.font.SysFont("Arial", 32)

    def update(self, screen):
        pass

    def render(self, screen):
        screen.fill(pg.Color("black"))
        title_words = "Bweakowt"
        subtitle_words = "[ press Space to start ]"
        title_text = self.title_font.render(title_words, True, pg.Color("white"))
        subtitle_text = self.subtitle_font.render(subtitle_words, True, pg.Color("white"))
        screen.blit(title_text, [(SCREEN_SIZE[0] / 2) - (self.title_font.size(title_words)[0] / 2), 100])
        screen.blit(subtitle_text, [(SCREEN_SIZE[0] / 2) - (self.subtitle_font.size(subtitle_words)[0] / 2), 300])

    def handle_events(self, events):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.manager.goto(LevelScene(1))
                elif e.key == pg.K_SPACE:
                    pg.quit()
                    sys.exit()


class SceneManager(object):
    def __init__(self):
        self.scene = Scene()
        self.goto(TitleScene())

    def goto(self, scene):
        self.scene = scene
        self.scene.manager = self

if __name__ == "__main__":
    pg.init()
    pg.display.set_caption(CAPTION)
    screen = pg.display.set_mode(SCREEN_SIZE)
    manager = SceneManager()
    while True:
        manager.scene.handle_events(pg.event.get())
        manager.scene.update(screen)
        manager.scene.render(screen)
        pg.display.flip()
