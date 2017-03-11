import argparse
import json
import os
import tempfile

import requests

from mistral_lint import suite


parser = argparse.ArgumentParser(description='')

parser.add_argument('--review', default=None, help=(
    "Provide the ID for a OpenStack gerrit review. It will be downloaded and "
    "linted - the paths argument will be ignored in this case."))
parser.add_argument('paths', nargs='*', help=(
    "A set of local paths to lint."))


def _download_review(review_id):

    GERRIT_URL = ("https://review.openstack.org/changes/?q={}"
                  "&o=DOWNLOAD_COMMANDS&o=CURRENT_REVISION")

    change = requests.get(GERRIT_URL.format(review_id)).content[5:]
    change = json.loads(change)[0]
    current = change['current_revision']
    change = change['revisions'][current]['fetch']['anonymous http']

    url = change['url']
    ref = change['ref']

    with tempfile.TemporaryDirectory() as tmpdirname:
        os.system('git clone {} {}'.format(url, tmpdirname))
        os.system('cd {}; git fetch {} {}; git checkout FETCH_HEAD'.format(
            tmpdirname, url, ref))

        suite.lint([tmpdirname, ])


def main():
    args = parser.parse_args()

    if args.review:
        _download_review(args.review)
    elif args.paths:
        suite.lint(args.paths)


if __name__ == "__main__":
    main()
