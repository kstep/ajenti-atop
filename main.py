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
    METRICS = ['CPU', 'DSK', 'CPL', 'NET', 'MEM', 'SWP']

    def init(self):
        self.title = 'ATop'
        self.icon = 'signal'
        self.category = _('Software')

        self.samples = []

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
                elif point._multikey:
                    sample.setdefault(name, {}).setdefault(key, []).append(point)
                else:
                    sample.setdefault(name, {})[key] = point

    def atop(self, logfile, *sections):
        args = ['/usr/bin/atop', '-P', ','.join(sections)]
        if logfile:
            args.extend(('-r', logfile))

        return Popen(args, stdout=PIPE)

    def load_atop(self, logfile, sections, filter_=list):
        atop = self.atop(logfile, *sections)

        try:
            samples = self.parse_atop(iter(atop.stdout.readline, ''))
            next(samples)
        except StopIteration:
            return []

        return filter_(samples)

    @on('loadlog', 'click')
    def loadlog(self):
        if self._stream:
            self.context.notify('info', 'Turn off live stream first')
            return

        logfile = self.find('logfile').value
        self.samples = self.load_atop(logfile, self.METRICS)

        if not self.samples:
            self.context.notify('error', 'Not enough atop data to load')

        self.binder.populate()

    _stream = False
    def worker(self):
        samples = self.load_atop(None, self.METRICS)

        for sample in samples:
            if not self._stream:
                break

            self.samples.append(sample)

            if len(self.samples) > 144:
                self.samples.pop(0)

            self.binder.populate()

        atop.kill()

    @on('livestream', 'click')
    def livestream(self):
        self._stream = not self._stream

        if self._stream:
            self.samples = []
            self.context.session.spawn(self.worker)

        self.find('livestream').pressed = self._stream
