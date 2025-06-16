import stage
import random
import time
import supervisor


import constants


def splash_scene():
    coin_sound = open("coin.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)
    sound.play(coin_sound)

    image_bank = stage.Bank.from_bmp16("mt_game_studio.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    background.tile(2, 2, 0)
    background.tile(3, 2, 1)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = [background]
    game.render_block()

    time.sleep(2.0)
    menu_scene()


def menu_scene():
    image_bank = stage.Bank.from_bmp16("space_aliens_background.bmp")
    background = stage.Grid(
        image_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    text = []
    text1 = stage.Text(width=29, height=14)
    text1.move(20, 20)
    text1.text("DAISY & CO.")
    text.append(text1)

    text2 = stage.Text(width=29, height=14)
    text2.move(30, 60)
    text2.text("PRESS START")
    text.append(text2)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_START:
            game_scene()
        game.tick()


def game_scene():
    image_bank_background = stage.Bank.from_bmp16("space_aliens_background.bmp")
    image_bank_sprites = stage.Bank.from_bmp16("space_aliens.bmp")

    a_button = constants.button_state["button_up"]
    lives = constants.STARTING_LIVES
    score = 0

    pew_sound = open("pew2.wav", "rb")
    boom_sound = open("boom.wav", "rb")
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    background = stage.Grid(
        image_bank_background, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )
    ship = stage.Sprite(
        image_bank_sprites, 5, 75, constants.SCREEN_Y - (2 * constants.SPRITE_SIZE)
    )

    lasers = []
    for _ in range(constants.TOTAL_NUMBER_OF_LASERS):
        laser = stage.Sprite(
            image_bank_sprites, 10, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        lasers.append(laser)

    aliens = []
    alien_directions = []
    for _ in range(constants.TOTAL_NUMBER_OF_ALIENS):
        alien = stage.Sprite(
            image_bank_sprites, 9, constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
        )
        aliens.append(alien)
        alien_directions.append({"x": 0, "y": 0})

    def show_alien():
        for i in range(len(aliens)):
            if aliens[i].x < 0:
                rand_x = random.randint(0, constants.SCREEN_X - constants.SPRITE_SIZE)
                aliens[i].move(rand_x, constants.OFF_TOP_SCREEN)
                alien_directions[i]["x"] = random.choice([-1, 0, 1])
                alien_directions[i]["y"] = random.randint(1, 2)
                break

    def game_over_scene(final_score):
        sound.stop()
        image_bank2 = stage.Bank.from_bmp16("mt_game_studio.bmp")
        background = stage.Grid(
            image_bank2, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
        )

        text = []
        text1 = stage.Text(
            width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
        )
        text1.move(20, 20)
        text1.text("Final Score: {:0>2d}".format(final_score))
        text.append(text1)

        text2 = stage.Text(
            width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
        )
        text2.move(40, 60)
        text2.text("GAME OVER")
        text.append(text2)

        text3 = stage.Text(
            width=29, height=14, font=None, palette=constants.BLUE_PALETTE, buffer=None
        )
        text3.move(23, 110)
        text3.text("PRESS SELECT")
        text.append(text3)

        game = stage.Stage(ugame.display, constants.FPS)
        game.layers = text + [background]
        game.render_block()

        while True:
            keys = ugame.buttons.get_pressed()
            if keys & ugame.K_START:
                game_scene()
            game.tick()

    show_alien()

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = aliens + lasers + [ship] + [background]
    game.render_block()

    while True:
        keys = ugame.buttons.get_pressed()

        # Ship movement


if keys & ugame.K_RIGHT:
    if ship.x <= constants.SCREEN_X - constants.SPRITE_SIZE:
        ship.move(ship.x + constants.SPRITE_MOVEMENT_SPEED, ship.y)
    else:
        ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)


if keys & ugame.K_LEFT:
    if ship.x >= 0:
        ship.move(ship.x - constants.SPRITE_MOVEMENT_SPEED, ship.y)
    else:
        ship.move(0, ship.y)


if keys & ugame.K_UP:
    ship.move(ship.x, max(0, ship.y - constants.SPRITE_MOVEMENT_SPEED))
if keys & ugame.K_DOWN:
    ship.move(
        ship.x,
        min(
            constants.SCREEN_Y - constants.SPRITE_SIZE,
            ship.y + constants.SPRITE_MOVEMENT_SPEED,
        ),
    )


# Laser fire handling
if keys & ugame.K_X:
    if a_button == constants.button_state["button_up"]:
        a_button = constants.button_state["button_just_pressed"]
    elif a_button == constants.button_state["button_just_pressed"]:
        a_button = constants.button_state["button_still_pressed"]
else:
    if a_button == constants.button_state["button_still_pressed"]:
        a_button = constants.button_state["button_released"]
    else:
        a_button = constants.button_state["button_up"]


if a_button == constants.button_state["button_just_pressed"]:
    for laser in lasers:
        if laser.x < 0:
            laser.move(ship.x + 6, ship.y)
            sound.play(pew_sound)
            break


# Move lasers
for laser in lasers:
    if laser.x > 0:
        laser.move(laser.x, laser.y - constants.LASER_SPEED)
        if laser.y < constants.OFF_TOP_SCREEN:
            laser.move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)


# Move aliens
for i in range(len(aliens)):
    if aliens[i].x > 0:
        new_x = aliens[i].x + alien_directions[i]["x"]
        new_y = aliens[i].y + alien_directions[i]["y"]

        # Bounce off side borders
        if new_x <= 0 or new_x >= constants.SCREEN_X - constants.SPRITE_SIZE:
            alien_directions[i]["x"] *= -1
            new_x = aliens[i].x + alien_directions[i]["x"]
            new_y += 5  # descend slightly when changing direction

        aliens[i].move(new_x, new_y)

        if new_y > constants.SCREEN_Y:
            lives -= 1
            aliens[i].move(constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y)
            if lives <= 0:
                game_over_scene(score)
            else:
                show_alien()


# Laser vs Alien collision
for laser_number in range(len(lasers)):
    if lasers[laser_number].x > 0:
        for alien_number in range(len(aliens)):
            if aliens[alien_number].x > 0:
                if stage.collide(
                    lasers[laser_number].x + 6,
                    lasers[laser_number].y + 2,
                    lasers[laser_number].x + 11,
                    lasers[laser_number].y + 12,
                    aliens[alien_number].x + 1,
                    aliens[alien_number].y,
                    aliens[alien_number].x + 15,
                    aliens[alien_number].y + 15,
                ):
                    aliens[alien_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
                    lasers[laser_number].move(
                        constants.OFF_SCREEN_X, constants.OFF_SCREEN_Y
                    )
                    sound.stop()
                    sound.play(boom_sound)
                    show_alien()
                    score += 1


# Alien vs Ship collision
for alien_number in range(len(aliens)):
    if aliens[alien_number].x > 0:
        if stage.collide(
            aliens[alien_number].x + 1,
            aliens[alien_number].y,
            aliens[alien_number].x + 15,
            aliens[alien_number].y + 15,
            ship.x + 1,
            ship.y,
            ship.x + 15,
            ship.y + 15,
        ):
            sound.stop()
            sound.play(boom_sound)
            time.sleep(1.0)
            game_over_scene(score)


game.render_sprites(aliens + lasers + [ship])
game.tick()


if __name__ == "__main__":
    splash_scene()
