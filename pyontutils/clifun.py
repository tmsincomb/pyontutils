"""Helper classes for organizing docopt programs
Usage:
    demo [options] <args>...

Options:
    -o --optional      an optional argument
"""


class Options:
    # there is only ever one of these because of how docopt works
    def __new__(cls, args, defaults):
        cls.args = args
        cls.defaults = defaults
        for arg, value in cls.args.items():
            ident = python_identifier(arg.strip('-'))

            @property
            def options_property(self, value=value):
                f""" {arg} {value} """
                return value

            if hasattr(cls, ident):  # complex logic in properties
                ident = '_default_' + ident

            setattr(cls, ident, options_property)

        return super().__new__(cls)

    @property
    def commands(self):
        for k, v in self.args.items():
            if v and not any(k.startswith(c) for c in ('-', '<')):
                yield k

    def __repr__(self):
        def key(kv, counter=[0]):
            k, v = kv
            counter[0] += 1
            return (not bool(v),
                    k.startswith('-'),
                    k.startswith('<'),
                    counter[0] if not any(k.startswith(c) for c in ('-', '<')) else 0,
                    k)

        rows = [[k, '' if v is None or v is False
                 else ('x' if v is True
                       else ('_' if isinstance(v, list) else v))]
                for k, v in sorted([(k, v) for k, v in self.args.items()
                                    if v or k.startswith('-')
                ], key=key)
        ]
        atable = AsciiTable([['arg', '']] + rows, title='spc args')
        atable.justify_columns[1] = 'center'
        return atable.table

class Dispatcher:
    port_attrs = tuple()  # request from above
    child_port_attrs = tuple()  # force on below
    parent = None
    def __init__(self, options_or_parent, port_attrs=tuple()):
        if isinstance(options_or_parent, Dispatcher):
            parent = options_or_parent
            self.parent = parent
            self.options = parent.options
            if not port_attrs:
                port_attrs = self.port_attrs

            all_attrs = set(parent.child_port_attrs) | set(port_attrs)
            for attr in all_attrs:
                setattr(self, attr, getattr(parent, attr))  # fail if any are missing

        else:
            self.options = options_or_parent

    def __call__(self):
        # FIXME this might fail to run annos -> shell correctly
        first = self.parent is not None
        for command in self.options.commands:
            if first:
                first = False
                # FIXME this only works for 1 level
                continue  # skip the parent argument which we know will be true

            getattr(self, command)()
            return

        else:
            self.default()

    def default(self):
        raise NotImplementedError('docopt I can\'t believe you\'ve done this')


def main():
    from docopt import docopt, parse_defaults
    args = docopt(__doc__, version='clifun-demo 0.0.0')
    defaults = {o.name:o.value if o.argcount else None for o in parse_defaults(__doc__)}
    options = Options(args, defaults)
    main = Dispatcher(options)
    if main.options.debug:
        print(main.options)

    main()


if __name__ == '__main__':
    main()
