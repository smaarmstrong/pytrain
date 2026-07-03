import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="calc", description="A tiny calculator.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add two integers")
    p_add.add_argument("a", type=int)
    p_add.add_argument("b", type=int)

    p_div = sub.add_parser("div", help="divide two floats")
    p_div.add_argument("a", type=float)
    p_div.add_argument("b", type=float)

    p_pow = sub.add_parser("pow", help="raise an integer to a power")
    p_pow.add_argument("base", type=int)
    p_pow.add_argument("--exp", type=int, default=2)

    args = parser.parse_args(argv)
    if args.command == "add":
        print(args.a + args.b)
    elif args.command == "div":
        print(args.a / args.b)
    else:
        print(args.base ** args.exp)


if __name__ == "__main__":
    main()
