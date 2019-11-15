"""jc - JSON CLI output utility uname Parser

Usage:
    specify --uname as the first argument if the piped input is coming from uname

Limitations:
    must use 'uname -a'

Example:

    $ uname -a | jc --uname -p
    {
      "kernel_name": "Linux",
      "node_name": "user-ubuntu",
      "kernel_release": "4.15.0-65-generic",
      "operating_system": "GNU/Linux",
      "hardware_platform": "x86_64",
      "processor": "x86_64",
      "machine": "x86_64",
      "kernel_version": "#74-Ubuntu SMP Tue Sep 17 17:06:04 UTC 2019"
    }
"""
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

        {
            "kernel_name":        string,
            "node_name":          string,
            "kernel_release":     string,
            "operating_system":   string,
            "hardware_platform":  string,
            "processor":          string,
            "machine":            string,
            "kernel_version":     string
        }
    """
    # nothing to process
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, freebsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    raw_output = {}
    parsed_line = data.split(maxsplit=3)

    if len(parsed_line) > 1:

        raw_output['kernel_name'] = parsed_line.pop(0)
        raw_output['node_name'] = parsed_line.pop(0)
        raw_output['kernel_release'] = parsed_line.pop(0)

        parsed_line = parsed_line[-1].rsplit(maxsplit=4)

        raw_output['operating_system'] = parsed_line.pop(-1)
        raw_output['hardware_platform'] = parsed_line.pop(-1)
        raw_output['processor'] = parsed_line.pop(-1)
        raw_output['machine'] = parsed_line.pop(-1)

        raw_output['kernel_version'] = parsed_line.pop(0)

    if raw:
        return raw_output
    else:
        return process(raw_output)
