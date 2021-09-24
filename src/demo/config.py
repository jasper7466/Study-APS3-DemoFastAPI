from pathlib import Path
from dynaconf import Dynaconf


PROJECT_ROOT = Path(__file__).parents[2]

settings = Dynaconf(
    envvar_prefix="FASTAPI_DEMO",
    settings_files=['settings.toml', '.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
