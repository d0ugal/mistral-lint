import argparse

from mistral_lint import suite


parser = argparse.ArgumentParser(description='')
parser.add_argument('paths', nargs='+')


def main():
    args = parser.parse_args()
    suite.lint(args.paths)


if __name__ == "__main__":
    main()
