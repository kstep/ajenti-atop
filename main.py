from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder
from ajenti.ui import on, p, UIElement
from ajenti.plugins.atop.models import ATOP
from subprocess import Popen, PIPE

@p('type', type=str, default='line')
@p('title', type=str)
@p('subtitle', type=str, default='')
@p('data', bindtypes=[list], default=[])
@p('series', type=eval, default=[])
@p('xaxis', type=eval, default=[])
@p('yaxis', type=eval, default=[])
@p('width', default=None)
@p('height', default=None)
@plugin
class Chart(UIElement):
    typeid = 'chart'

@plugin
class ATop(SectionPlugin):
    def init(self):
        self.title = 'ATop'
        self.icon = 'signal'
        self.category = _('Software')

        self.cpustats = []

        self.append(self.ui.inflate('atop:main'))
        self.binder = Binder(self, self.find('main'))

    @on('loadlog', 'click')
    def loadlog(self):
        logfile = self.find('logfile').value
        data, _ = Popen(['/usr/bin/atop', '-r', logfile, '-P', 'CPU'], stdout=PIPE).communicate()
        self.cpustats = [ATOP.parse(line) for line in data.splitlines() if line not in ('SEP', 'RESET')][1:]
        self.binder.populate()

