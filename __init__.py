from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa

info = PluginInfo(
    title='ATop',
    icon='signal',
    dependencies=[
        PluginDependency('main'),
        PluginDependency('models'),
        BinaryDependency('atop'),
    ],
)

def init():
    import main
