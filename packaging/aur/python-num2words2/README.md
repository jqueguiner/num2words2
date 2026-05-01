# AUR package: `python-num2words2`

Files in this directory mirror what needs to live in the AUR git repo at
`ssh://aur@aur.archlinux.org/python-num2words2.git`.

## One-time AUR setup

1. Create an AUR account: https://aur.archlinux.org/register
2. Add your SSH public key to that account (Account → My Account → Edit → SSH
   Public Key).
3. Verify SSH access: `ssh aur@aur.archlinux.org help` should print a help banner.

## First-time publish

```bash
# Clone the empty AUR repo for the new package name. The first push creates it.
git clone ssh://aur@aur.archlinux.org/python-num2words2.git
cd python-num2words2

# Copy PKGBUILD + .SRCINFO from this directory.
cp /path/to/num2words2/packaging/aur/python-num2words2/PKGBUILD .
cp /path/to/num2words2/packaging/aur/python-num2words2/.SRCINFO .

# Sanity-check locally on an Arch box (or makepkg in a container).
makepkg --syncdeps --clean
namcap PKGBUILD
namcap python-num2words2-1.0.3-1-any.pkg.tar.zst

git add PKGBUILD .SRCINFO
git commit -m "Initial import: python-num2words2 1.0.3"
git push origin master
```

The package will appear at https://aur.archlinux.org/packages/python-num2words2
within a minute.

## Updating to a new release

When a new num2words2 version ships to PyPI:

1. Bump `pkgver` in `PKGBUILD` (and reset `pkgrel=1`).
2. Refresh the sha256:
   ```bash
   curl -sL https://files.pythonhosted.org/packages/source/n/num2words2/num2words2-${NEWVER}.tar.gz \
     | sha256sum
   ```
   Paste the value into `sha256sums=(...)`.
3. Regenerate `.SRCINFO`:
   ```bash
   makepkg --printsrcinfo > .SRCINFO
   ```
4. Commit + push:
   ```bash
   git commit -am "Bump to ${NEWVER}"
   git push
   ```

## Automating release bumps

Once the package is live, a GitHub Action in this repo can push updates
automatically when a new version tag is created. See `.github/workflows/aur-publish.yml`
(to be added).
