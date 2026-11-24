import json
import re
import hashlib
import argparse
from pathlib import Path
from urllib.parse import quote

from .config import RAW_DIR, PROCESSED_DIR, CHUNKS_PATH
from .chunking import section_chunks


SKIP_DIRS = {
    "node_modules",
    ".git",
    "images",
    "assets",
    "generated",
    "gitlab-handbook",
}


def clean_markdown(text: str) -> str:
    """Remove common Markdown boilerplate and normalize whitespace."""
    text = re.sub(r'^---\s*\n.*?\n---\s*\n', '', text, flags=re.S)
    text = re.sub(r'\[TOC\]|\[toc\]', '', text, flags=re.I)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def iter_markdown(root: Path):
    """Yield Markdown files while excluding unwanted directories."""
    for p in root.rglob('*.md'):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def page_url(path: Path, root: Path) -> str:
    """
    Generate the original GitLab documentation URL.

    Supports:
    1. The original nested doc directory structure.
    2. Our flattened handbook_subset filenames:
       security_filename.md
       administration_filename.md
       user_filename.md
    3. The starter demo corpus.
    """

    path = Path(path)
    root = Path(root)

    # Starter/demo corpus
    if 'demo_corpus' in root.parts or 'demo_corpus' in path.parts:
        return 'https://example.invalid/policypilot-demo/' + quote(path.name)

    # Flattened GitLab corpus
    filename = path.name

    categories = {
        'security_': 'security',
        'administration_': 'administration',
        'user_': 'user',
    }

    for prefix, category in categories.items():
        if filename.startswith(prefix):
            original_filename = filename[len(prefix):]

            # Index files
            if original_filename == '_index.md':
                return (
                    'https://gitlab.com/gitlab-org/gitlab/-/tree/master/doc/'
                    + category
                )

            return (
                'https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/'
                + category
                + '/'
                + quote(original_filename)
            )

    # Original nested directory structure
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.name

    return (
        'https://gitlab.com/gitlab-org/gitlab/-/blob/master/doc/'
        + quote(rel)
    )


def build_chunks(
    root: Path = Path('data/raw/demo_corpus'),
    max_tokens: int = 320,
    overlap: int = 45,
) -> list[dict]:
    """Build metadata-rich chunks from Markdown documents."""

    root = Path(root)
    docs = list(iter_markdown(root))
    chunks = []

    for p in docs:
        raw = p.read_text(
            encoding='utf-8',
            errors='ignore',
        )

        cleaned = clean_markdown(raw)

        title = (
            p.stem
            .replace('-', ' ')
            .replace('_', ' ')
            .title()
        )

        found = re.search(r'^#\s+(.+)$', cleaned, re.M)

        if found:
            title = found.group(1).strip()

        chunks.extend(
            section_chunks(
                cleaned,
                title,
                page_url(p, root),
                str(p),
                max_tokens,
                overlap,
            )
        )

    # Stable chunk IDs
    for c in chunks:
        c['chunk_id'] = hashlib.sha1(
            (
                c['source_path']
                + c['section_path']
                + c['text']
            ).encode()
        ).hexdigest()[:12]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    CHUNKS_PATH.write_text(
        ''.join(
            json.dumps(c, ensure_ascii=False) + '\n'
            for c in chunks
        ),
        encoding='utf-8',
    )

    return chunks


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--root',
        default='data/raw/demo_corpus',
    )

    parser.add_argument(
        '--max-tokens',
        type=int,
        default=320,
    )

    parser.add_argument(
        '--overlap',
        type=int,
        default=45,
    )

    args = parser.parse_args()

    chunks = build_chunks(
        Path(args.root),
        args.max_tokens,
        args.overlap,
    )

    print(
        f'Built {len(chunks)} chunks from {args.root} '
        f'-> {CHUNKS_PATH}'
    )


if __name__ == '__main__':
    main()