from django.apps import AppConfig

from dongtai_common.common.utils import DongTaiAppConfigPatch


class IastConfig(DongTaiAppConfigPatch, AppConfig):
    name = "dongtai_web"

    def ready(self):
        super().ready()
        from deploy.commands.management.commands.load_hook_strategy import Command
        from dongtai_common.utils.init_schema import init_schema
        from dongtai_common.utils.validate import validate_hook_strategy_update
        from dongtai_conf.celery import app as celery_app  # noqa: F401
        from dongtai_conf.settings import AUTO_UPDATE_HOOK_STRATEGY

        # do not remove this import, used in celery
        from dongtai_engine.plugins.project_status import (  # noqa: F401
            update_project_status,
        )

        if AUTO_UPDATE_HOOK_STRATEGY and not validate_hook_strategy_update():
            print("enable auto_update_hook_strategy  updating hook strategy from file")  # noqa: T201
            Command().handle()

        init_schema()
