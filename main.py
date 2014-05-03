from ajenti.api import *  # noqa
from ajenti.plugins import *  # noqa
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui.binder import Binder
from ajenti.ui import on, p, UIElement
from ajenti.plugins.atop.models import ATOP
from subprocess import Popen, PIPE
from datetime import datetime

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

        self.stats = []

        self.append(self.ui.inflate('atop:main'))
        self.find('logfile').value = '/var/log/atop/atop_%s' % datetime.now().strftime('%Y%m%d')
        self.binder = Binder(self, self.find('main'))
        self.loadlog()

    @staticmethod
    def parse_atop(lines):
        sample = {}

        for line in lines:
            if line == 'RESET\n':
                sample = {}

            elif line == 'SEP\n':
                yield sample
                sample = {}

            else:
                point = ATOP.parse(line)
                sample.setdefault(point.__class__.__name__, []).append(point)

    @on('loadlog', 'click')
    def loadlog(self):
        logfile = self.find('logfile').value
        sections = ['CPU', 'DSK', 'CPL']
        atop = Popen(['/usr/bin/atop', '-r', logfile, '-P', ','.join(sections)], stdout=PIPE)

        stats = self.parse_atop(atop.stdout.readlines())
        next(stats)
        self.stats = list(stats)

        self.binder.populate()
