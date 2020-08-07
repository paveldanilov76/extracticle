import sys


def readline(msg='>'):
    return input(msg)


if __name__ == '__main__':
    print('"exit" for quit')
    inp = input('>')
    while inp != 'exit':
        try:
            sys.argv = sys.argv[:1] + inp.split()
            from extracticle import main, settings
            settings.args = settings.parser.parse_args()
            settings.conf = settings.Config()

            main.run()
        except:
            continue
        finally:
            inp = input('>')
