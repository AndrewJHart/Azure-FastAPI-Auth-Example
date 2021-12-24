from fastapi import FastAPI, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
from fastapi.templating import Jinja2Templates
from app.ms_utils import load_cache, save_cache, build_msal_app, build_auth_code_flow, get_token_from_cache
import app_config
import requests

# instantiate app
app = FastAPI()

# configure template engine
templates = Jinja2Templates(directory='templates')

# default ttl for mem cache
default_ttl = 10*60*60


def mem_cache():
    """
    sets default cache key for group
    """
    return caches.get(CACHE_KEY)


@app.on_event('startup')
async def on_startup() -> None:
    """
    simple event listener to configure & init local mem-cache

    :note: Redis would be perfect for this and this supports Redis or mem-cache
    :return: None
    """
    mem = InMemoryCacheBackend()
    caches.set(CACHE_KEY, mem)


@app.get('/')
async def index(
    request: Request,
    session_cache: InMemoryCacheBackend = Depends(mem_cache)
):
    # check cache for user
    user = await session_cache.get('user')

    if user:
        # user authenticated, render index with proper context
        return templates.TemplateResponse(
            'index.html',
            {'request': request, 'user': user, 'endpoint': True, 'version': msal.__version__}
        )

    # otherwise, no user/token so redirect to login page
    return RedirectResponse(app.url_path_for('login'))


@app.get('/login', response_class=HTMLResponse)
async def login(
    request: Request,
    session_cache: InMemoryCacheBackend = Depends(mem_cache)
):
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    flow = build_auth_code_flow(app, scopes=app_config.SCOPE)

    await session_cache.set('flow', flow, ttl=default_ttl)  # cache the flow for 10 hours or until app restarts

    cached_flow = await session_cache.get('flow')

    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'auth_url': cached_flow['auth_uri'], 'version': msal.__version__}
    )


@app.get('/oauth')  # Its absolute URL must match your app's redirect_uri set in AAD
async def authorized(
    request: Request,
    session_cache: InMemoryCacheBackend = Depends(mem_cache)
):
    try:
        cache = await load_cache(session_cache)  # pass our mem-cache as a session
        cached_flow = await session_cache.get('flow')

        # build the app config, pass cache store for success & pass the cached flow generated earlier
        # as well convert the query params to a dict (from the 3 way handshake that returns the code, etc...)
        result = build_msal_app(
            cache=cache
        ).acquire_token_by_auth_code_flow(
            cached_flow,
            dict(request.query_params)
        )

        if 'error' in result:
            return templates.TemplateResponse(
                'auth_error.html',
                {'request': request, 'result': result}
            )

        # auth was successful, set the user cache info & use this chance
        # to grab any other data you would need if you wanted to wrap
        # this in your own JSON Web Token
        await session_cache.set('user', result.get('id_token_claims'), ttl=default_ttl)
        await save_cache(cache, session_cache)
    except ValueError:  # Usually caused by CSRF
        pass  # ugh, ignore this. I don't like this Rich... Microsoft

    return RedirectResponse(app.url_path_for('index'))  # redirect back to index /


@app.get('/logout')
def logout(
    session_cache: InMemoryCacheBackend = Depends(mem_cache)
):
    session_cache.flush()  # flush out the mem-cache

    # construct the url to hit MS & logout user then redirect back to index page
    logout_redirect = '{authority}/oauth2/v2.0/logout?post_logout_redirect_uri={host}{index_page}'.format(
        authority=app_config.AUTHORITY,
        host=app_config.HOST_URL,
        index_page=app.url_path_for('index')
    )

    return RedirectResponse(logout_redirect)


@app.get('/graphcall')
async def graphcall(
    request: Request,
    session_cache: InMemoryCacheBackend = Depends(mem_cache)
):
    # attempt to fetch the token from our mem-cache
    token = await get_token_from_cache(session_cache, app_config.SCOPE)

    # uncomment to print the full token info
    # print(token)

    if not token:
        return RedirectResponse(app.url_path_for('login'))

    # use requests to relay api call from backend service to another service
    graph_data = requests.get(
        app_config.ENDPOINT,
        headers={'Authorization': 'Bearer ' + token['access_token']},
    ).json()

    return templates.TemplateResponse('display.html', {'request': request, 'result': graph_data})
