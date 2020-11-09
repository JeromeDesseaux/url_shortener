from fastapi import APIRouter
from models.url import Item
from starlette.responses import RedirectResponse
import redis
import uuid
import os


# On vérifie l'environnement du serveur (déployé ou dev)
try:
    is_deployed = os.environ['ENVIRONMENT'] == "production"
except KeyError:
    is_deployed = False

router = APIRouter()
# On démarre le connecteur redis sur la bonne instance selon l'environnement serveur
r = redis.Redis(host='redis' if is_deployed else 'localhost', port=6379)


@router.get('/')
def root():
    """ URL racine sans autre utilité que de dire un petit coucou aux utilisateurs """
    return {"message": "Welcome to our URL shortener app"}

@router.post('/shortify')
def shorten_url(item: Item):
    """ 
    Raccourci une URL passée en paramètre. 
    Retourne la valeur contenue dans REDIS si déjà existante, 
    en créé une nouvelle et la stocke sinon 
    """
    url = item.url
    redis_url = r.get(url)
    if redis_url is None:
        shorten_url = item.custom_target or str(uuid.uuid4())[-6:]
        if r.mset({url: shorten_url}):
            return {"url": url, "short": shorten_url}
        return {"message": "failed"}
    return {"message": "URL already exists", "short": redis_url}


@router.get("/{short}")
def redirect_url(short: str):
    """
    Redirige les utilisateurs vers le site initial avant raccourcissement de l'URL
    """
    for key in r.keys():
        if r.get(key).decode("utf8") == short:
            return RedirectResponse(url=key.decode("utf8"))
    return {"message": "URL not defined"}