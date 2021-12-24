import os

CLIENT_ID = "<client id>"  # Application (client) ID of app registration

CLIENT_SECRET = "<client secret value>"  # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = "https://login.microsoftonline.com/07a204b0-4ada-44d7-8ebd-9d168f38a08c"  # For multi-tenant app
# AUTHORITY = "https://login.microsoftonline.com/Enter_the_Tenant_Name_Here"

HOST_URL = "http://localhost:9000"
REDIRECT_PATH = "/oauth"  # Used for forming an absolute URL to your redirect URI.
                          # The absolute URL must match the redirect URI you set
                          # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["User.ReadBasic.All"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
