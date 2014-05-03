from ajenti.plugins.models.api import *  # noqa

brackets = lambda n: str(n)[1:-1]
boolflag = lambda y: y == 'y'

class ATOP(Model):
    _fields = ['host', 'epoch', 'date', 'time', 'interval']
    _casts = {
            'host': str,
            'epoch': int,
            'date': timestamp('%Y-%m-%d'),
            'time': timestamp('%H:%M:%S'),
            'interval': timedelta
            }

    _labels = {}
    class __metaclass__(Model.__metaclass__):
        def __init__(cls, name, bases, attrs):
            Model.__metaclass__.__init__(cls, name, bases, attrs)
            cls._labels[name] = cls

    @property
    def key(self):
        return None

    @classmethod
    def parse(cls, line):
        parts = line.split()
        label = parts.pop(0)

        if label in ('RESET', 'SEP'):
            return

        label_cls = cls._labels[label]
        data = dict(zip(label_cls._fields, parts))
        return label_cls(**data)


class CPU(ATOP):
    _fields = ATOP._fields + ['tps', 'ncpu', 'sys', 'usr', 'nice', 'idle', 'wait', 'irq', 'sirq', 'steal', 'guest', 'freq', 'pfreq']
    _casts = {
            'tps': int,
            'ncpu': int,
            'sys': int,
            'usr': int,
            'nice': int,
            'idle': int,
            'wait': int,
            'irq': int,
            'sirq': int,
            'steal': int,
            'guest': int,
            'freq': int,
            'pfreq': int,
            }

class CPL(ATOP):
    _fields = ATOP._fields + ['nproc', 'la1', 'la5', 'la15', 'ctx', 'int']
    _casts = {
            'nproc': int,
            'la1': float,
            'la5': float,
            'la15': float,
            'ctx': int,
            'int': int,
            }

class MEM(ATOP):
    _fields = ATOP._fields + ['page', 'phys', 'free', 'cache', 'buffer', 'slab', 'dirty', 'rslab']
    _casts = {
            'page': int,
            'phys': int,
            'free': int,
            'cache': int,
            'buffer': int,
            'slab': int,
            'dirty': int,
            'rslab': int,
            }

class SWP(ATOP):
    _fields = ATOP._fields + ['page', 'swap', 'free', '_', 'cmt', 'lcmt']
    _casts = {
            'page': int,
            'swap': int,
            'free': int,
            '_': int,
            'cmt': int,
            'lcmt': int,
            }

class PAG(ATOP):
    _fields = ATOP._fields + ['page', 'scans', 'alloc', '_', 'swin', 'swout']
    _casts = {
            'page': int,
            'scans': int,
            'alloc': int,
            '_': int,
            'swin': int,
            'swout': int,
            }

class DSK(ATOP):
    _fields = ATOP._fields + ['name', 'iotime', 'reads', 'sread', 'writes', 'swrite']
    _casts = {
            'name': str,
            'iotime': int,
            'reads': int,
            'sread': int,
            'writes': int,
            'swrite': int,
            }

    @property
    def key(self):
        return self.name

class MDD(DSK):
    pass

class LVM(DSK):
    pass

class NET(ATOP):
    _fields = ATOP._fields + ['label', 'tcprcv', 'tcpsnd', 'udprcv', 'udpsnd', 'iprcv', 'ipsnd', 'ipfwd']
    _casts = {
            'label': str,
            'tcprcv': int,
            'tcpsnd': int,
            'udprcv': int,
            'udpsnd': int,
            'iprcv': int,
            'ipsnd': int,
            'ipfwd': int,
            }

    @property
    def key(self):
        return self.label

class NETIF(ATOP):
    _fields = ATOP._fields + ['name', 'prcv', 'brcv', 'psnd', 'bsnd', 'speed', 'mode']
    _casts = {
            'name': str,
            'prcv': int,
            'brcv': int,
            'psnd': int,
            'bsnd': int,
            'speed': int,
            'mode': compose(int, ['half', 'full'].__getitem__)
            }

    @property
    def key(self):
        return self.name

class PROC(ATOP):
    _fields = ATOP._fields + ['pid', 'name', 'state']
    _casts = {
            'pid': int,
            'name': brackets,
            'state': str,
            }

    @property
    def key(self):
        return self.pid

class PRG(PROC):
    _fields = PROC._fields + ['ruid', 'rgid', 'tgid', 'thrn', 'code', 'start', 'fname', 'ppid', 'thrr', 'thri', 'thru', 'euid', 'egid', 'suid', 'sgid', 'fuid', 'fgid', 'eta']
    _casts = {
            'ruid': int,
            'rgid': int,
            'tgid': int,
            'thrn': int,
            'code': int,
            'start': unixtime,
            'fname': brackets,
            'ppid': int,
            'thrr': int,
            'thri': int,
            'thru': int,
            'euid': int,
            'egid': int,
            'suid': int,
            'sgid': int,
            'fuid': int,
            'fgid': int,
            'eta': unixtime,
            'isproc': boolflag,
            }

class PRC(PROC):
    _fields = PROC._fields + ['tps', 'usr', 'sys', 'nice', 'pri', 'rtpri', 'sched', 'cpu', 'savg', 'tgid']
    _casts = {
            'tps': int,
            'usr': int,
            'sys': int,
            'nice': int,
            'pri': int,
            'rtpri': int,
            'sched': int,
            'cpu': int,
            'savg': int,
            'tgid': int,
            'isproc': boolflag,
            }

class PRM(PROC):
    _fields = PROC._fields + ['page', 'virt', 'rss', 'shrd', 'virtd', 'rssd', 'minflt', 'majflt', 'vlib', 'vdata', 'vstack', 'swap', 'tgid']
    _casts = {
            'page': int,
            'virt': int,
            'rss': int,
            'shrd': int,
            'virtd': int,
            'rssd': int,
            'minflt': int,
            'majflt': int,
            'vlib': int,
            'vdata': int,
            'vstack': int,
            'swap': int,
            'tgid': int,
            'isproc': boolflag,
            }

class PRD(PROC):
    _fields = ATOP._fields + ['okp', 'stdio', 'reads', 'sread', 'writes', 'swrite', 'cwrite', 'tgid']
    _casts = {
            'okp': boolflag,
            'stdio': boolflag,
            'reads': int,
            'sread': int,
            'writes': int,
            'swrite': int,
            'cwrite': int,
            'tgid': int,
            'isproc': boolflag,
            }

class PRN(PROC):
    _fields = ATOP._fields + ['netatop', 'tcpsnd', 'ctcpsnd', 'tcprcv', 'ctcprcv', 'udpsnd', 'cudpsnd', 'udprcv', 'cudprcv', 'rawsnd', 'rawrcv', 'tgid']
    _casts = {
            'netatop': boolflag,
            'tcpsnd': int,
            'ctcpsnd': int,
            'tcprcv': int,
            'ctcprcv': int,
            'udpsnd': int,
            'cudpsnd': int,
            'udprcv': int,
            'cudprcv': int,
            'rawsnd': int,
            'rawrcv': int,
            'tgid': int,
            'isproc': boolflag,
            }

#class RESET(ATOP):
    #pass

#class SEP(ATOP):
    #pass

