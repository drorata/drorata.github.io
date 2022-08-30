# Publishing the website:

Basically, three steps are needed:

1. First, build the site locally
2. Prepare the static built (use [ghp-import](https://github.com/davisp/ghp-import))
3. Push to `master`

These steps can be accomplished using:

```bash
pelican content -o output -s publishconf.py
ghp-import output
git push git@github.com:drorata/drorata.github.io.git gh-pages:master
```

For the sake of simplicity and fun, [`Taskfile`](./Taskfile.yaml) is available.

To make things even better, a GitHub Action [`.github/workflows/deploy_pages.yml`](./.github/workflows/deploy_pages.yml) is also there.
Every push to `source` branch will trigger the building of the site and publishing it.
