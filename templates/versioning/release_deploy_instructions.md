

# Version and Deploy Release

>Follow these internal instructions to provide a central release that other repos can call and consume.

Use these commands from the root of the repository.

## Prerequisites

Confirm GitHub CLI authentication:

```
gh auth status
```

Update the local default branch:

```
git switch main
git pull --ff-only
```

Confirm there are no uncommitted changes:

```
git status --short
```

Update `RELEASE_NOTES.md` before creating the release.

## Create a release candidate

Use a release-candidate version such as `v1.0.0-rc.1`:

```
gh release create v1.0.0-rc.1 --repo vinas1/docs --target main --title "My Release Name v1.0.0-rc.1" --prerelease --notes-file RELEASE_NOTES.md
```

View the prerelease:

```
gh release view v1.0.0-rc.1 --repo vinas1/docs
```

Consumers test it with:

```
uses: vinas1/docs/.github/workflows/my-resuable-workflow-name.yml@v1.0.0-rc.1
```

## Create the stable release

After the release candidate has been successfully tested, create the stable release:

```
gh release create v1.0.0 --repo vinas1/docs --target main --title "My Release Name v1.0.0" --latest --notes-file RELEASE_NOTES.md
```

View the latest stable release:

```
gh release view `
  --repo vinas1/docs
```

Consumers use the stable version with:

```
uses: vinas1/docs/.github/workflows/my-resuable-workflow-name.yml@v1.0.0
```

## List all releases

```
gh release list `
  --repo vinas1/docs
```

## Verify a tagged workflow

Confirm that a release tag contains the reusable workflow:

```
gh api `
  --method GET `
  "repos/vinas1/docs/contents/.github/workflows/my-resuable-workflow-name.yml" -f "ref=v1.0.0" --jq '.path'
```

Expected output:

```
.github/workflows/my-resuable-workflow-name.yml
```

## Delete an incorrect release

Only use this when a release was created with the wrong tag or from the wrong commit:

```
gh release delete v1.0.0 `
  --repo vinas1/docs `
  --cleanup-tag `
  --yes
```

## Version rules

- Release candidate: `v1.0.0-rc.1`
- Patch release: `v1.0.1`
- Minor release: `v1.1.0`
- Breaking release: `v2.0.0`
- Do not use a stable tag for a prerelease.
- Do not reuse or move a published tag.
- Consumers should pin an exact version instead of `main`.
