"""jc - JSON CLI output utility `foo` command output streaming parser

> This streaming parser outputs JSON Lines

<<Short foo description and caveats>>

Usage (cli):

    $ foo | jc --foo-s

Usage (module):

    import jc
    # result is an iterable object (generator)
    result = jc.parse('foo_s', foo_command_output.splitlines())
    for item in result:
        # do something

    or

    import jc.parsers.foo_s
    # result is an iterable object (generator)
    result = jc.parsers.foo_s.parse(foo_command_output.splitlines())
    for item in result:
        # do something

Schema:

    {
      "foo":            string,

      # Below object only exists if using -qq or ignore_exceptions=True

      "_jc_meta":
        {
          "success":    boolean,     # false if error parsing
          "error":      string,      # exists if "success" is false
          "line":       string       # exists if "success" is false
        }
    }

Examples:

    $ foo | jc --foo-s
    {example output}
    ...

    $ foo | jc --foo-s -r
    {example output}
    ...
"""
from typing import Dict, Iterable
import jc.utils
from jc.utils import stream_success, stream_error
from jc.exceptions import ParseError


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.0'
    description = '`foo` command streaming parser'
    author = 'John Doe'
    author_email = 'johndoe@gmail.com'

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']
    streaming = True


__version__ = info.version


def _process(proc_data: Dict) -> Dict:
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """

    # process the data here
    # rebuild output for added semantic information
    # use helper functions in jc.utils for int, float,
    # bool conversions and timestamps

    return proc_data


def parse(
    data: Iterable[str],
    raw: bool = False,
    quiet: bool = False,
    ignore_exceptions: bool = False
) -> Iterable[Dict]:
    """
    Main text parsing generator function. Returns an iterator object.

    Parameters:

        data:              (iterable)  line-based text data to parse
                                       (e.g. sys.stdin or str.splitlines())

        raw:               (boolean)   unprocessed output if True
        quiet:             (boolean)   suppress warning messages if True
        ignore_exceptions: (boolean)   ignore parsing exceptions if True

    Yields:

        Dictionary. Raw or processed structured data.

    Returns:

        Iterator object
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.streaming_input_type_check(data)

    for line in data:
        output_line: Dict = {}
        try:
            jc.utils.streaming_line_input_type_check(line)

            # parse the content here
            # check out helper functions in jc.utils
            # and jc.parsers.universal

            if output_line:
                yield stream_success(output_line, ignore_exceptions) if raw else stream_success(_process(output_line), ignore_exceptions)
            else:
                raise ParseError('Not foo data')

        except Exception as e:
            yield stream_error(e, ignore_exceptions, line)
