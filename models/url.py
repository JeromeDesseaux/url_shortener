from pydantic import BaseModel


class Item(BaseModel):
    """ Définition de la classe de représentation des URL complètes et raccourcies """
    url: str
    custom_target: str = None