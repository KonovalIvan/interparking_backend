import sys
import pkgutil
import inspect

ALLOWED_IMPORTS = {
    "app.domain": ["app.domain"],  # domain może widzieć tylko siebie
    "app.application": ["app.domain", "app.application"],  # application może widzieć domenę
    "app.infrastructure": ["app.domain", "app.application", "app.infrastructure"],  # infra widzi wszystko
    "app.api": ["app.application", "app.api"],  # API może widzieć application
}


def module_name(file):
    return file.__name__.split(".")[0] + "." + ".".join(file.__name__.split(".")[1:3])


def run_layer_guard():
    """
    Sprawdza IMPORTY i wyrzuca błąd jeśli:
      - domena importuje infra lub api
      - api importuje infra
      - application importuje api
    """
    for module in list(sys.modules.values()):
        if not hasattr(module, "__file__"):
            continue

        name = module.__name__
        parts = name.split(".")

        if len(parts) < 3:
            continue

        base = ".".join(parts[:2])  # np. app.domain

        if base not in ALLOWED_IMPORTS:
            continue

        allowed_prefixes = ALLOWED_IMPORTS[base]

        source = inspect.getsource(module)
        for line in source.splitlines():
            if line.strip().startswith("import") or line.strip().startswith("from"):
                for forbidden in ["app.infrastructure", "app.api"]:
                    if forbidden in line and forbidden not in allowed_prefixes:
                        raise ImportError(
                            f"❌ WARSTWA NARUSZONA!\n"
                            f"Moduł {name} NIE MOŻE importować {forbidden}\n"
                            f"Linia: {line}"
                        )
