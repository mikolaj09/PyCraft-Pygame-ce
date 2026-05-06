import pymunk


def get_space_instance():
    new_space = pymunk.Space()
    new_space.iterations = 60
    new_space.collision_persistence = 20
    new_space.gravity = (0, 1000)
    return new_space


space_instance = get_space_instance()
