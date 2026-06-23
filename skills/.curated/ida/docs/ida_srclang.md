# ida_srclang

Third-party compiler support for parsing type declarations from C/C++/Objective-C source.

## Key Functions

### Parser Selection
- `select_parser_by_name(name)` - Set parser by name (None/"" for default)
- `select_parser_by_srclang(lang)` - Set parser supporting language(s)
- `get_selected_parser_name()` - Get current parser name

### Type Declaration Parsing
- `parse_decls_for_srclang(lang, til, input, is_path)` - Parse with language auto-detection
- `parse_decls_with_parser(parser_name, til, input, is_path)` - Parse with specific parser
- `parse_decls_with_parser_ext(parser_name, til, input, hti_flags)` - Parse with formatting flags

**Parameters:**
- `lang/parser_name` - Source language or parser name
- `til` - Type library to store parsed types
- `input` - File path or declaration string
- `is_path` - True if input is path, False if in-memory snippet

**Returns:**
- -1: No parser found
- -2: Operation not supported (set_parser_argv)
- >=0: Number of parse errors

### Parser Configuration
- `set_parser_argv(parser_name, argv)` - Set command-line arguments
- `get_parser_option(parser_name, option_name)` - Get parser option
- `set_parser_option(parser_name, option_name, option_value)` - Set parser option

## Source Languages

- `SRCLANG_C` - C
- `SRCLANG_CPP` - C++
- `SRCLANG_OBJC` - Objective-C
- `SRCLANG_SWIFT` - Swift (not supported yet)
- `SRCLANG_GO` - Golang (not supported yet)

## See Also
Full docs: skill/docs/ida_srclang.rst
