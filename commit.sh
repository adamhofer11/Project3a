#!/bin/bash

set -e

BRANCH="main"

git_add_commit_push() {
    if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        printf "Error: Not a git repository.\n" >&2
        return 1
    fi

    if ! git diff --quiet || ! git diff --cached --quiet; then
        git add .
        if ! git commit -m "Update via bash script"; then
            printf "Error: Git commit failed.\n" >&2
            return 1
        fi
    else
        printf "No changes to commit.\n"
        return 0
    fi

    if ! git push origin "$BRANCH"; then
        printf "Error: Git push failed.\n" >&2
        return 1
    fi

    printf "Pushed to Git successfully.\n"
}

main() {
    git_add_commit_push
}

main