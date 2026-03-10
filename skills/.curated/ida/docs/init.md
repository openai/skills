# init

IDAPython initialization and execution environment module.

## Key Classes/Functions

### IDAPythonStdOut
Dummy file-like class that receives stdout and stderr
- `write(text)` - writes text to IDA's output window
- `flush()` - flush output
- `isatty()` - returns False (not a TTY)

### runscript(script)
Executes a script file (deprecated, use `idaapi.IDAPython_ExecScript()` instead)
- `script` - path to script file
- Returns error string or None on success

### print_banner()
Prints IDAPython banner to output window

## Attributes
- `base` - Python installation base path
- `IDAPYTHON_DYNLOAD_BASE` - dynamic load base directory
- `help` - IDAPython help instance
- `userrc` - user RC file path

## See Also
Full docs: skill/docs/init.rst
