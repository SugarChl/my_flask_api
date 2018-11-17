from .Article import article
from .User import user
from .Activity import activity
from .Search import search
from .Attention import attention
from .History import history
from .HomePage import homepage
# 蓝本配置
DEFAULT_BLUEPRINT = (
    # （蓝本，url前缀）
    (article, '/api_1_0/article'),
    (user, '/api_1_0/user'),
    (activity, '/api_1_0/activity'),
    (search, '/api_1_0/search'),
    (attention, "/api_1_0/attention"),
    (history, "/api_1_0/history"),
    (homepage, "/api_1_0/homepage")
)


# 封装函数完成蓝本注册
def config_blueprint(app):
    for blueprint, url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint, url_prefix=url_prefix)