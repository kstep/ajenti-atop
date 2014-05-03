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
        self.disk_stats = []

        self.append(self.ui.inflate('atop:main'))
        self.find('logfile').value = '/var/log/atop/atop_%s' % datetime.now().strftime('%Y%m%d')

    def on_first_page_load(self):
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
                point = ATOP(line)
                name, key = point.__class__.__name__, point.key
                if key is None:
                    sample[name] = point
                else:
                    sample.setdefault(name, {})[key] = point

    @on('loadlog', 'click')
    def loadlog(self):
        logfile = self.find('logfile').value
        sections = ['CPU', 'DSK', 'CPL']
        atop = Popen(['/usr/bin/atop', '-r', logfile, '-P', ','.join(sections)], stdout=PIPE)

        try:
            stats = self.parse_atop(atop.stdout.readlines())
            next(stats)
            self.stats = list(stats)
        except StopIteration:
            self.context.notify('error', 'Not enough atop data to load')

        else:
            self.selectdisk()

    @on('selectdisk', 'click')
    def selectdisk(self):
        try:
            disk_name = self.find('disk_name').value
            self.disk_stats = map(lambda s: s['DSK'][disk_name], self.stats)
        except KeyError:
            self.context.notify('info', 'Please select a disk to show stats')
        finally:
            self.binder.populate()

