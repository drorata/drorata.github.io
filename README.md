# Publishing the website:

Three steps:

1. First, build the site locally:
2. Prepare the static built (use [ghp-import](https://github.com/davisp/ghp-import))
3. Push to `master`

```bash
pelican content -o output -s publishconf.py
ghp-import output
git push git@github.com:drorata/drorata.github.io.git gh-pages:master
```
