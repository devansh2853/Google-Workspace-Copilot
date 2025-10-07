from constants import composio

def create_auth_config(slug):
    config = composio.auth_configs.create(
    toolkit=slug,
    options = {
        'type': "use_composio_managed_auth",
        'auth_scheme': "OAUTH2",
        }
    )
    return config

gmail_auth_config = create_auth_config("GMAIL")
docs_auth_config = create_auth_config("GOOGLEDOCS")
sheets_auth_config = create_auth_config("googlesheets")
slides_auth_config = create_auth_config("googleslides")

print(f"""
GMAIL_AUTH_CONFIG_ID={gmail_auth_config.id}
DOCS_AUTH_CONFIG_ID={docs_auth_config.id}
SHEETS_AUTH_CONFIG_ID={sheets_auth_config.id}
SLIDES_AUTH_CONFIG_ID={slides_auth_config.id}
""")



