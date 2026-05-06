import pygame
import pymunk.pygame_util
import random
import configparser
import queue
import loader
import sprites
import text
import effects
import display
import world
import space
import block_types
import item_types
import light_engine
from player import Player
from constants import *


class App:

    """Main class of the engine. There no arguments you could give.
    The run method launches the application."""

    def __init__(self):
        self.display = None
        self.clock = None
        self.game_settings = None
        self.volume = None
        self.language = None
        self.debug_mode = None
        self.seed = None
        self.game_world = None
        self.state = None

    def run(self):

        pygame.init()
        display.display = display.Display()
        self.display = display.display
        self.clock = pygame.time.Clock()

        self.game_settings = loader.load_settings('config.ini')
        self.volume = self.game_settings[VOLUME]
        self.language = self.game_settings[LANGUAGE]

        block_types.BlockTypes.load_from_json()
        item_types.ItemTypes.load_from_json()

        ui_sprites_loaded = queue.Queue()
        blocks_sprites_loaded = queue.Queue()
        items_sprites_loaded = queue.Queue()
        player_sprites_loaded = queue.Queue()
        entity_sprites_loaded = queue.Queue()

        ui_graphic_thread = loader.start_loading(ui_sprites_loaded, 'ui_graphics')
        blocks_graphics_thread = loader.start_loading(blocks_sprites_loaded, 'blocks_graphics', BLOCK_SIZE / 8)
        items_sprites_thread = loader.start_loading(items_sprites_loaded, 'items_graphics', ITEM_SIZE / 8)
        player_sprites_thread = loader.start_loading(player_sprites_loaded, 'player_graphics')
        entity_sprites_thread = loader.start_loading(entity_sprites_loaded, 'entity_graphics')

        ui_graphic_thread.start()
        blocks_graphics_thread.start()
        items_sprites_thread.start()
        player_sprites_thread.start()
        entity_sprites_thread.start()

        self.loading_menu(ui_graphic_thread, blocks_graphics_thread, items_sprites_thread, player_sprites_thread, entity_sprites_thread)

        ui_graphic_thread.join()
        blocks_graphics_thread.join()
        items_sprites_thread.join()
        player_sprites_thread.join()
        entity_sprites_thread.join()

        sprites.Sprites.load(ui_sprites_loaded, blocks_sprites_loaded, items_sprites_loaded, player_sprites_loaded, entity_sprites_loaded)

        block_types.BlockTypes.load(sprites.Sprites.BLOCKS)
        item_types.ItemTypes.load(sprites.Sprites.ITEMS)

        self.completed_loading_menu()
        self.menu()

    def game(self, mode=NEW_WORLD):

        if mode == NEW_WORLD:
            space.space_instance = space.get_space_instance()
            world.world_instance = world.World(self.game_settings[WORLD_TYPE], self.seed, self.game_settings[GAME_MODE])
            self.game_world = world.world_instance
            self.game_world.generate_new_world()
        elif mode == RESTART_WORLD:
            space.space_instance = space.get_space_instance()
            world.world_instance = world.World(self.game_settings[WORLD_TYPE], self.seed, self.game_settings[GAME_MODE])
            self.game_world = world.world_instance
            self.game_world.generate_new_world()
        elif mode == OLD_WORLD:
            self.game_world.respawn()
            space.space_instance = space.get_space_instance()

        if self.debug_mode:
            draw_options = pymunk.pygame_util.DrawOptions(self.display.screen)
        else:
            draw_options = None

        player = Player(self.game_settings[GAME_MODE])
        player.spawn()
        self.display.fill((0, 0, 0))
        fps_text = text.Text((10, 10), 12, (255, 255, 255))
        position_text = text.Text((10, 24), 12, (255, 255, 255))
        current_fps = FPS
        player.total_offset = [0, 0]
        player.give_item(item_name=ITEM_SAND, amount=64)
        player.give_item(item_name=ITEM_DIRT, amount=64)
        player.give_item(item_name=ITEM_GLOWSTONE, amount=64)

        game_time = 0

        while player.alive:

            mouse_position = pygame.mouse.get_pos()
            mouse_button_event = [False] * 3
            mouse_button_pressed = pygame.mouse.get_pressed()
            keys1 = pygame.key.get_pressed()
            keys2 = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    keys2 = event.key
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    if event.key == pygame.K_q:
                        player.kill()
                    if event.key == pygame.K_r:
                        player.give_item(item_name=DIRT, amount=64)
                    if event.key == pygame.K_y:
                        light_engine.LightCell.day_light = light_engine.LightCell.day_light + 1 if light_engine.LightCell.day_light < light_engine.MAX_LIGHT else light_engine.MAX_LIGHT
                    if event.key == pygame.K_h:
                        light_engine.LightCell.day_light = light_engine.LightCell.day_light - 1 if light_engine.LightCell.day_light > 0 else 0
                    if event.key == pygame.K_i:
                        player.player_stats.experience += 1
                    if event.key == pygame.K_k:
                        player.player_stats.level += 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_button_event[0] = True
                    if event.button == 2:
                        mouse_button_event[1] = True
                    if event.button == 3:
                        mouse_button_event[2] = True

            player.update(keys1, keys2, mouse_position, mouse_button_event, mouse_button_pressed)
            self.game_world.update(player, mouse_position)

            fps_text.change_text(str(current_fps) + 'fps')

            display.display.draw(player, self.game_world)

            if self.debug_mode:
                space.space_instance.debug_draw(draw_options)

            x = self.game_world.camera.last_displacement[0] // BLOCK_SIZE
            y = WORLD_HEIGHT - self.game_world.camera.last_displacement[1] // BLOCK_SIZE - 12
            a = self.game_world.get_x_y_world(tuple(player.total_offset))[0] - 118
            b = self.game_world.chunk_start_index - (ORIGINAL_WORLD_SIZE - CHUNK_SIZE) // 2

            position_text.change_text(f'X/Y: {x}/{a}/{y}/{b}')
            fps_text.draw()
            position_text.draw()
            pygame.display.update()
            space.space_instance.step(1 / FPS)
            game_time += 1 / current_fps if current_fps != 0 else 0
            self.clock.tick(FPS)
            current_fps = round(self.clock.get_fps())

        if not player.alive:
            self.dead_message()

    def loading_menu(self, *graphic_threads):

        background_loading = pygame.image.load('preloader/background_loading.png').convert_alpha()
        loading_spinner = pygame.image.load('preloader/loading1.png').convert_alpha()

        dots = ''
        loading_text = text.Text((10, self.display.height - 50), 40, (255, 255, 255))
        while any(thread.is_alive() for thread in graphic_threads):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            display.display.blit(background_loading, (0, 0))
            display.display.blit(loading_spinner, (self.display.width - 110, self.display.height - 110))
            loading_spinner = pygame.transform.rotate(loading_spinner, -90)
            loading_text.change_text(f'Loading{dots} PLEASE WAIT!')
            loading_text.draw()
            dots = dots + '.' if len(dots) <= 3 else ''

            pygame.display.update()
            self.clock.tick(FPS // 25)

    def completed_loading_menu(self):
        print('loading completed')
        self.display.fill((0, 0, 0))

        continue_text = text.Text((self.display.width // 2, self.display.height // 2), 32, (255, 255, 255), text='TO CONTINUE PRESS ENTER')
        colors = ((255, 255, 255), (0, 255, 0))
        selected_color = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            continue_text.draw(align='center')
            continue_text.change_color(colors[selected_color])
            selected_color = not selected_color

            pygame.display.update()
            self.clock.tick(FPS // 10)

    def menu(self):

        background_menu = None

        ui_sprites = sprites.Sprites.UI

        for i in ui_sprites:

            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        buttons_texts = [text.Text((self.display.width // 2 - 150, 462), 32, (255, 255, 255), text='START'),
                         text.Text((self.display.width // 2 - 150, 612), 32, (255, 255, 255), text='SETTINGS'),
                         text.Text((self.display.width // 2 - 150, 762), 32, (255, 255, 255), text='EXIT')]

        title_text = text.Text((self.display.width // 2, 150), 128, (0, 255, 0), text=APPLICATION_NAME)

        version_text = text.Text((self.display.width - 4, self.display.height - 20), 16, (255, 255, 255), text=APPLICATION_NAME + ' ' + VERSION)

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        selected_button = 0

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 2:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 2

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            self.start_game()
                        elif selected_button == 1:
                            self.menu_settings()
                            retro_effects.clear()
                        else:
                            pygame.quit()
                            exit()

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()
            retro_effects.random_glitch()
            retro_effects.draw_glitch()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text

            title_text.draw(align='center')
            version_text.draw(align='topright')

            pygame.display.update()
            self.clock.tick(FPS)

    def start_game(self):

        buttons_texts = [text.Text((self.display.width // 2 - 150, 462), 32, (255, 255, 255), text='NEW GAME'),
                         text.Text((self.display.width // 2 - 150, 612), 32, (255, 255, 255), text='LOAD GAME'),
                         text.Text((self.display.width // 2 - 150, 762), 32, (255, 255, 255), text='BACK')]

        selected_button = 0

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 2:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 2

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            self.new_game()
                        elif selected_button == 1:
                            self.load_game()
                        else:
                            self.menu()

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text

            pygame.display.update()
            self.clock.tick(FPS)

    def new_game(self):

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        world_types = ['NORMAL', 'FLAT']
        difficulty = ['EASY', 'MEDIUM', 'HARD', 'IMPOSSIBLE']
        generate_structures = ['ON', 'OFF']
        game_modes = [SURVIVAL, CREATIVE, SPECTATOR]
        debug_modes = ['OFF', 'ON']
        seed = str(random.randint(0, 10 ** 14))
        settings = {WORLD_TYPE: 'NORMAL', DIFFICULTY: 'MEDIUM', GENERATE_STRUCTURES: 'ON',
                    GAME_MODE: 'SURVIVAL'}

        self.game_settings = settings | self.game_settings

        debug_mode = False

        buttons_texts = [text.Text((self.display.width // 2 - 275, 312), 32, (255, 255, 255), text='WORLD TYPE: ' + str(settings[WORLD_TYPE])),
                         text.Text((self.display.width // 2 - 275, 412), 32, (255, 255, 255), text='DIFFICULTY: ' + str(settings[DIFFICULTY])),
                         text.Text((self.display.width // 2 - 275, 512), 32, (255, 255, 255), text='GENERATE STRUCTURES: ' + str(settings[GENERATE_STRUCTURES])),
                         text.Text((self.display.width // 2 - 275, 612), 32, (255, 255, 255), text='GAME MODE: ' + str(settings[GAME_MODE])),
                         text.Text((self.display.width // 2 - 275, 712), 32, (255, 255, 255), text='SEED: ' + str(seed)),
                         text.Text((self.display.width // 2 - 275, 812), 32, (255, 255, 255), text='DEBUG_MODE: ' + debug_modes[0]),
                         text.Text((self.display.width // 2 - 400, 912), 32, (255, 255, 255), text='BACK'),
                         text.Text((self.display.width // 2 - 400, 212), 32, (255, 255, 255), text='START')]

        pointer_text = text.Text((self.display.width // 2 - 275, 712), 32, (255, 255, 255), text='_')
        pointer_position = pointer_text.position
        pointer_position_x = 8 + len(seed)
        j = 0

        selected_button = 0

        buttons = 7

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > buttons:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = buttons

                    if event.key == pygame.K_RIGHT:
                        if selected_button == 0:
                            i = world_types.index(settings[WORLD_TYPE])
                            if i + 1 < len(world_types):
                                settings[WORLD_TYPE] = world_types[i + 1]
                            else:
                                settings[WORLD_TYPE] = world_types[0]

                        elif selected_button == 1:
                            i = difficulty.index(settings[DIFFICULTY])
                            if i + 1 < len(difficulty):
                                settings[DIFFICULTY] = difficulty[i + 1]
                            else:
                                settings[DIFFICULTY] = difficulty[0]

                        elif selected_button == 2:
                            i = generate_structures.index(settings[GENERATE_STRUCTURES])
                            if i + 1 < len(generate_structures):
                                settings[GENERATE_STRUCTURES] = generate_structures[i + 1]
                            else:
                                settings[GENERATE_STRUCTURES] = generate_structures[0]

                        elif selected_button == 3:
                            i = game_modes.index(settings[GAME_MODE])
                            if i + 1 < len(game_modes):
                                settings[GAME_MODE] = game_modes[i + 1]
                            else:
                                settings[GAME_MODE] = game_modes[0]

                        elif selected_button == 5:
                            debug_mode = not debug_mode

                    if event.key == pygame.K_LEFT:
                        if selected_button == 0:
                            i = world_types.index(settings[WORLD_TYPE])
                            if i - 1 >= 0:
                                settings[WORLD_TYPE] = world_types[i - 1]
                            else:
                                settings[WORLD_TYPE] = world_types[-1]

                        elif selected_button == 1:
                            i = difficulty.index(settings[DIFFICULTY])
                            if i - 1 >= 0:
                                settings[DIFFICULTY] = difficulty[i - 1]
                            else:
                                settings[DIFFICULTY] = difficulty[-1]

                        elif selected_button == 2:
                            i = generate_structures.index(settings[GENERATE_STRUCTURES])
                            if i - 1 >= 0:
                                settings[GENERATE_STRUCTURES] = generate_structures[i - 1]
                            else:
                                settings[GENERATE_STRUCTURES] = generate_structures[-1]

                        elif selected_button == 3:
                            i = game_modes.index(settings[GAME_MODE])
                            if i - 1 >= 0:
                                settings[GAME_MODE] = game_modes[i - 1]
                            else:
                                settings[GAME_MODE] = game_modes[-1]

                        elif selected_button == 5:
                            debug_mode = not debug_mode

                    if len(seed) < 15 and pygame.key.name(event.key).isnumeric() and selected_button == 4:
                        seed = seed[:pointer_position_x - 8] + pygame.key.name(event.key) + seed[pointer_position_x - 8:]
                        pointer_position_x += 1

                    if event.key == pygame.K_BACKSPACE and selected_button == 4:
                        seed = seed[:pointer_position_x - 9] + seed[pointer_position_x - 8:]
                        pointer_position_x -= 1

                    if event.key == pygame.K_RIGHT and selected_button == 4:
                        pointer_position_x += 1

                    if event.key == pygame.K_LEFT and selected_button == 4:
                        pointer_position_x -= 1

                    pointer_position_x = 8 if pointer_position_x < 8 else len(seed) + 8 if pointer_position_x > len(seed) + 8 else pointer_position_x

                    if event.key == pygame.K_RETURN:
                        if selected_button == 6:
                            self.start_game()
                        elif selected_button == 7:
                            self.game(mode=NEW_WORLD)

                    self.seed = int(seed) if seed.isnumeric() else None
                    self.debug_mode = debug_mode
                    buttons_texts[0].change_text('WORLD TYPE: ' + str(settings[WORLD_TYPE]))
                    buttons_texts[1].change_text('DIFFICULTY: ' + str(settings[DIFFICULTY]))
                    buttons_texts[2].change_text('GENERATE STRUCTURES: ' + str(settings[GENERATE_STRUCTURES]))
                    buttons_texts[3].change_text('GAME MODE: ' + str(settings[GAME_MODE]))
                    buttons_texts[4].change_text('SEED: ' + str(seed))
                    buttons_texts[5].change_text('DEBUG_MODE: ' + debug_modes[debug_mode])

            self.game_settings = settings

            j = 0 if j > 120 else j + 1
            pointer_text.change_position((pointer_position[0] + pointer_position_x * 32, pointer_text.position[1]))

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text

            if j >= 60 and selected_button == 4:
                pointer_text.draw()

            pygame.display.update()
            self.clock.tick(FPS)

    def load_game(self):
        pass

    def controls(self):
        buttons_texts = [text.Text((self.display.width // 2 - 300, 412), 32, (255, 255, 255), text='BACK'),
                         text.Text((self.display.width // 2 - 300, 512), 32, (255, 255, 255), text='LEFT: L'),
                         text.Text((self.display.width // 2 - 300, 612), 32, (255, 255, 255), text='RIGHT: D'),
                         text.Text((self.display.width // 2 - 300, 712), 32, (255, 255, 255), text='SNEAK: SHIFT'),
                         text.Text((self.display.width // 2 - 300, 812), 32, (255, 255, 255), text='JUMP: SPACE')]

        selected_button = 0

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 4:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 4

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 4:
                            return

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text

            pygame.display.update()
            self.clock.tick(FPS)

    def menu_settings(self):

        buttons_texts = [text.Text((self.display.width // 2 - 300, 362), 32, (255, 255, 255), text='VOLUME: ' + str(self.volume)),
                         text.Text((self.display.width // 2 - 300, 512), 32, (255, 255, 255), text='LANGUAGE: ' + str(self.language)),
                         text.Text((self.display.width // 2 - 300, 662), 32, (255, 255, 255), text='CONTROLS'),
                         text.Text((self.display.width // 2 - 300, 812), 32, (255, 255, 255), text='BACK')]

        selected_button = 0

        volume = tuple(range(101))
        languages = [ENGLISH, POLISH]

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 3:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 3

                    if event.key == pygame.K_RIGHT:
                        if selected_button == 0:
                            i = volume.index(self.game_settings[VOLUME])
                            if i + 1 < len(volume):
                                self.game_settings[VOLUME] = volume[i + 1]
                            else:
                                self.game_settings[VOLUME] = volume[0]

                        elif selected_button == 1:
                            i = languages.index(self.game_settings[LANGUAGE])
                            if i + 1 < len(languages):
                                self.game_settings[LANGUAGE] = languages[i + 1]
                            else:
                                self.game_settings[LANGUAGE] = languages[0]

                    if event.key == pygame.K_LEFT:
                        if selected_button == 0:
                            i = volume.index(self.game_settings[VOLUME])
                            if i - 1 >= 0:
                                self.game_settings[VOLUME] = volume[i - 1]
                            else:
                                self.game_settings[VOLUME] = volume[-1]

                        elif selected_button == 1:
                            i = languages.index(self.game_settings[LANGUAGE])
                            if i - 1 >= 0:
                                self.game_settings[LANGUAGE] = languages[i - 1]
                            else:
                                self.game_settings[LANGUAGE] = languages[-1]

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 2:
                            self.controls()
                        elif selected_button == 3:
                            self.save_settings('config.ini')
                            self.menu()

                    self.volume = self.game_settings[VOLUME]
                    self.language = self.game_settings[LANGUAGE]
                    buttons_texts[0].change_text('VOLUME: ' + str(self.volume))
                    buttons_texts[1].change_text('LANGUAGE: ' + str(self.language))

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text

            pygame.display.update()
            self.clock.tick(FPS)

    def save_settings(self, filename):
        config = configparser.ConfigParser()

        config[SETTINGS] = {
            VOLUME: str(self.game_settings[VOLUME]),
            LANGUAGE: self.game_settings[LANGUAGE],
        }

        with open(filename, 'w') as configfile:
            config.write(configfile)

    def pause(self):

        buttons_texts = [text.Text((self.display.width // 2 - 150, 462), 32, (255, 255, 255), text='RESUME'),
                         text.Text((self.display.width // 2 - 150, 612), 32, (255, 255, 255), text='RESTART'),
                         text.Text((self.display.width // 2 - 150, 762), 32, (255, 255, 255), text='BACK TO MENU')]

        text1 = text.Text((self.display.width // 2, 262), 64, (255, 255, 255), text='GAME PAUSED')

        selected_button = 0

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 2:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 2

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            running = False
                        elif selected_button == 1:
                            self.game(mode=RESTART_WORLD)
                        elif selected_button == 2:
                            self.menu()

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text
            text1.draw(align='center')

            pygame.display.update()
            self.clock.tick(FPS)

    def dead_message(self):

        buttons_texts = [text.Text((self.display.width // 2 - 150, 462), 32, (255, 255, 255), text='RESPAWN'),
                         text.Text((self.display.width // 2 - 150, 612), 32, (255, 255, 255), text='BACK TO MENU')]

        text1 = text.Text((self.display.width // 2, 262), 64, (255, 255, 255), text='You died!')

        selected_button = 0

        for i in sprites.Sprites.UI:
            if i[NAME] == 'background_menu.png':
                background_menu = i[SURFACE]

        retro_effects = effects.RetroEffects()
        retro_effects.load_matrix_effect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_button += 1
                        if selected_button > 1:
                            selected_button = 0
                    if event.key == pygame.K_UP:
                        selected_button -= 1
                        if selected_button < 0:
                            selected_button = 1

                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:
                            self.game(mode=OLD_WORLD)
                        elif selected_button == 1:
                            self.menu()

            self.display.blit(background_menu, (0, 0))

            retro_effects.draw_matrix_effect()
            retro_effects.clear_matrix_effect()

            for index, button_text in enumerate(buttons_texts):
                if selected_button == index:
                    button_text.change_color((0, 255, 0))
                    if '> ' not in button_text.text:
                        button_text.change_text('> ' + button_text.text)
                else:
                    if '> ' in button_text.text:
                        button_text.text = button_text.text[2:]
                    button_text.change_color((255, 255, 255))
                button_text.draw()
                buttons_texts[index] = button_text
            text1.draw(align='center')

            pygame.display.update()
            self.clock.tick(FPS)
