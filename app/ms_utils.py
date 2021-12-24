import app_config
import msal

# default ttl for mem cache
default_ttl = 10*60*60


async def load_cache(session_cache):
    cache = msal.SerializableTokenCache()

    token_cache = await session_cache.get('token_cache')

    if token_cache:
        cache.deserialize(token_cache)

    return cache


async def save_cache(cache, session_cache):
    if cache.has_state_changed:
        await session_cache.set('token_cache', cache.serialize(), ttl=default_ttl)


def build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID,
        authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET,
        token_cache=cache
    )


def build_auth_code_flow(app, authority=None, scopes=None):
    """
    Must build full url here - suggest using config for varying environments but
    fastApi does not use the full url for url_path_for

    :note: There is a better way using the app to get base url - this is a hack in app_config (HOST_URL)

    :param app: instance of the Fast API app
    :param authority:
    :param scopes:
    :return:
    """
    redirect_url = str.format(
        '{host_url}{authorized}',
        host_url=app_config.HOST_URL,
        authorized=app.url_path_for('authorized')
    )

    return build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or [],
        redirect_uri=redirect_url
    )


async def get_token_from_cache(session_cache, scope=None):
    # This web app maintains one cache per session
    cache = await load_cache(session_cache)
    cca = build_msal_app(cache=cache)
    accounts = cca.get_accounts()

    # uncomment to print all accounts
    # print('accounts are: ', accounts)

    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        await save_cache(cache, session_cache)
        return result
