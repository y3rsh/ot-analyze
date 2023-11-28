# bump_version.py
import re
import subprocess


def fetch_latest_tags():
    # Fetch tags from the remote repository
    subprocess.run(["git", "fetch", "--tags"], check=True)


def get_latest_tag():
    try:
        # Fetch the latest tags from the remote
        fetch_latest_tags()

        # List all tags and filter version tags
        tags = subprocess.run(["git", "tag"], capture_output=True, text=True, check=True)
        version_tags = [tag for tag in tags.stdout.split("\n") if re.match(r"^v\d+\.\d+$", tag)]

        # Sort tags and get the latest
        latest_tag = sorted(version_tags, key=lambda x: [int(part) for part in x[1:].split(".")])[-1]
        return latest_tag
    except Exception:
        return "v0.0"


def bump_version(tag):
    major, minor = map(int, tag[1:].split("."))
    return f"v{major}.{minor + 1}"


def main():
    latest_tag = get_latest_tag()
    new_version = bump_version(latest_tag)
    # Execute git commands
    subprocess.run(["git", "add", "."], check=True)
    try:
        subprocess.run(["git", "diff", "--quiet"], check=True)
    except subprocess.CalledProcessError:
        print("No changes to commit")
        exit(0)
    subprocess.run(["git", "commit", "-m", new_version], check=True)
    subprocess.run(["git", "tag", "-a", "-m", new_version, new_version], check=True)
    subprocess.run(["git", "push", "--follow-tags"], check=True)

    print(f"Updated to {new_version}")


if __name__ == "__main__":
    main()
