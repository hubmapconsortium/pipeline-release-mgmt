from argparse import ArgumentParser

def tag_release_pipeline(tag: str, pretend: bool = False):
    pass

def main():
    p = ArgumentParser()
    p.add_argument(
        'tag',
        help="""
            Tag name to use, both in the pipeline Git repository and for
            any Docker images built for this pipeline.
        """,
    )
    p.add_argument(
        '--pretend',
        action='store_true',
        help="""
            Run in pretend mode: don't actually execute anything (tagging or 
            pushing commits, building, tagging, or pushing container images).
        """,
    )
    args = p.parse_args()

    tag_release_pipeline(args.tag, args.pretend)

if __name__ == '__main__':
    main()
