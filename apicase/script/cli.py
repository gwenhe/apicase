import argparse
from apicase import __description__, __version__


def main():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="显示版本"
    )
    #
    # subparsers = parser.add_subparsers(help="sub-command help")
    # sub_parser_run = init_parser_run(subparsers)
    # sub_parser_scaffold = init_parser_scaffold(subparsers)
    # sub_parser_har2case = init_har2case_parser(subparsers)
    # sub_parser_make = init_make_parser(subparsers)
    #
    # if len(sys.argv) == 1:
    #     # httprunner
    #     parser.print_help()
    #     sys.exit(0)
    # elif len(sys.argv) == 2:
    #     # print help for sub-commands
    #     if sys.argv[1] in ["-V", "--version"]:
    #         # httprunner -V
    #         print(f"{__version__}")
    #     elif sys.argv[1] in ["-h", "--help"]:
    #         # httprunner -h
    #         parser.print_help()
    #     elif sys.argv[1] == "startproject":
    #         # httprunner startproject
    #         sub_parser_scaffold.print_help()
    #     elif sys.argv[1] == "har2case":
    #         # httprunner har2case
    #         sub_parser_har2case.print_help()
    #     elif sys.argv[1] == "run":
    #         # httprunner run
    #         pytest.main(["-h"])
    #     elif sys.argv[1] == "make":
    #         # httprunner make
    #         sub_parser_make.print_help()
    #     sys.exit(0)
    # elif (
    #         len(sys.argv) == 3 and sys.argv[1] == "run" and sys.argv[2] in ["-h", "--help"]
    # ):
    #     # httprunner run -h
    #     pytest.main(["-h"])
    #     sys.exit(0)
    #
    # extra_args = []
    # if len(sys.argv) >= 2 and sys.argv[1] in ["run", "locusts"]:
    #     args, extra_args = parser.parse_known_args()
    # else:
    #     args = parser.parse_args()
    #
    # if args.version:
    #     print(f"{__version__}")
    #     sys.exit(0)
    #
    # if sys.argv[1] == "run":
    #     sys.exit(main_run(extra_args))
    # elif sys.argv[1] == "startproject":
    #     main_scaffold(args)
    # elif sys.argv[1] == "har2case":
    #     main_har2case(args)
    # elif sys.argv[1] == "make":
    #     main_make(args.testcase_path)
