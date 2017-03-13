from __future__ import print_function

import argparse
import json
import subprocess
import sys
import tempfile

import requests

from mistral_lint import suite


parser = argparse.ArgumentParser(description='')

parser.add_argument('--review', default=None, help=(
    "Provide the ID for a OpenStack gerrit review. It will be downloaded and "
    "linted - the paths argument will be ignored in this case."))
parser.add_argument('--diff', action="store_true", help=(
    "Used with --review to show the diff between the patch and its parent"))
parser.add_argument('paths', nargs='*', help=(
    "A set of local paths to lint."))


def _download_review(review_id, diff):

    GERRIT_URL = ("https://review.openstack.org/changes/?q={}"
                  "&o=DOWNLOAD_COMMANDS&o=CURRENT_REVISION")

    change = requests.get(GERRIT_URL.format(review_id)).content[5:]
    change = json.loads(change)[0]
    current = change['current_revision']
    change = change['revisions'][current]['fetch']['anonymous http']

    url = change['url']
    ref = change['ref']

    with tempfile.TemporaryDirectory() as tmpdirname:
        subprocess.check_output(['git', 'clone', url, tmpdirname],
                                stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'fetch', url, ref], cwd=tmpdirname,
                                stderr=subprocess.STDOUT)
        subprocess.check_output(['git', 'checkout', 'FETCH_HEAD'],
                                cwd=tmpdirname, stderr=subprocess.STDOUT)
        messages_patch = suite.lint([tmpdirname, ], not diff)

        if diff:
            subprocess.check_output(['git', 'reset', 'HEAD^', '--hard'],
                                    cwd=tmpdirname, stderr=subprocess.STDOUT)
            messages_prev = suite.lint([tmpdirname, ], False)

        if not diff:
            if messages_patch:
                sys.exit(1)
            else:
                return

        prev_files = set(messages_prev.keys())
        patch_files = set(messages_patch.keys())
        prev_only = prev_files - patch_files
        patch_only = patch_files - prev_files
        both_revs = prev_files | patch_files

        for f in prev_only:
            print(f)
            for m in messages_prev[f]:
                print("-{}".format(m))
            print()

        for f in patch_only:
            print(f)
            for m in messages_patch[f]:
                print("+{}".format(m))
            print()

        for f in both_revs:
            prev_file = messages_prev[f] - messages_patch[f]
            patch_file = messages_patch[f] - messages_prev[f]
            for m in prev_file:
                print("-{}".format(m))
            for m in patch_file:
                print("+{}".format(m))

        if messages_patch:
            sys.exit(1)


def main():
    args = parser.parse_args()

    if args.review:
        _download_review(args.review, args.diff)
    elif args.paths:
        if suite.lint(args.paths):
            sys.exit(1)


if __name__ == "__main__":
    main()
