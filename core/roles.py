from rolepermissions.roles import AbstractUserRole


class PostModerator(AbstractUserRole):
    available_permissions = {
        'edit_post_without_author': True,
    }


class FilmModerator(AbstractUserRole):
    available_permissions = {
        'edit_films': True,
    }