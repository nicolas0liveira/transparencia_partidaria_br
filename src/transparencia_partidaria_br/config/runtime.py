from dataclasses import dataclass, asdict
import json

from transparencia_partidaria_br.config.env import CONFIG_PATH

# --------------------------------------
# CONFIG MODELS
# --------------------------------------

@dataclass
class CKANConfig:
    source: str = "tse"


@dataclass
class PathsConfig:
    data_raw: str = "data/raw"
    data_silver: str = "data/silver"
    data_gold: str = "data/gold"


@dataclass
class AppConfig:
    ckan: CKANConfig
    paths: PathsConfig


# --------------------------------------
# DEFAULT
# --------------------------------------

DEFAULT_CONFIG = AppConfig(
    ckan=CKANConfig(),
    paths=PathsConfig(),
)


# --------------------------------------
# LOAD / SAVE
# --------------------------------------

def load_config() -> AppConfig:
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text())

            return AppConfig(
                ckan=CKANConfig(**data.get("ckan", {})),
                paths=PathsConfig(**data.get("paths", {})),
            )

        except Exception:
            return DEFAULT_CONFIG

    return DEFAULT_CONFIG


def save_config(config: AppConfig):
    CONFIG_PATH.write_text(
        json.dumps(asdict(config), indent=2)
    )


# --------------------------------------
# CACHE (opcional, mas recomendado)
# --------------------------------------

_config_cache: AppConfig | None = None


def get_config() -> AppConfig:
    global _config_cache

    if _config_cache is None:
        _config_cache = load_config()

    return _config_cache


def reset_config_cache():
    global _config_cache
    _config_cache = None