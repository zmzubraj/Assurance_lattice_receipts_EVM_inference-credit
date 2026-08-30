# Official template provenance and preflight

Status: producer-side provenance record; not publisher certification or submission authorization.

- Official source URL: `https://www.frontiersin.org/design/zip/Frontiers_LaTeX_Templates.zip`
- Downloaded: 2026-08-30
- Archive SHA-256: `706459fb1a7cf1b54d6ec9ebb00696cfec6edf7ef87d7eb7f0cc6a1ece460747`
- Archive size: 839,916 bytes
- Template comment version: 3.4, generated 2022-06-14
- Current author-guideline page recommends the linked LaTeX templates; the official reference-style table lists Frontiers in Blockchain as Frontiers Harvard (author/date).

## Vendored files

| File | SHA-256 |
|---|---|
| `official-template/FrontiersinHarvard.cls` | `5d0653546d3adb8fbc21e57948e762636f2193c9bb11e22d25c3d7c334843fa6` |
| `official-template/Frontiers-Harvard.bst` | `f08f8fb7b5d5a7613416e5c1ba7979dd88356f785b0f292ee9dde95bc2c53cda` |
| `official-template/logo1.pdf` | `9e9c680917b89a79a7649b587f382eeb1ecf1e3dcea6505c344e8324c427548d` |
| `official-template/frontiers-example.tex` | `73a4ff19eda637c285c1980a2fa46adaaac61fbcb104421baa07584031725ece` |

## Static security preflight

The archive member list and all `.tex`, `.cls`, and `.bst` files were inspected before compilation. No path traversal, shell-escape request, dynamic download-and-execute, credential access, destructive filesystem operation, obfuscation, or suspicious executable was found in the reviewed surfaces. Standard LaTeX auxiliary-file writes and package imports were present. Compilation is permitted only with shell escape disabled. This review does not claim the archive is universally clean or cryptographically publisher-signed.

The official class and bibliography style are preserved byte-for-byte. The project-specific manuscript is a separate file and does not modify publisher class/style files.

## Reviewed compatibility assets

The official class declared three packages absent from the local TeX Live subset. Their CTAN source archives were downloaded to a temporary directory, checked for path traversal and dangerous execution patterns, and only the required generated styles were vendored:

| Source/archive | Archive SHA-256 | Vendored files |
|---|---|---|
| `https://mirrors.ctan.org/macros/latex/contrib/sttools.zip` | `02569ee68ceec7548b7888add2da0dfa2574cb7097696eb3a2b458e08e999586` | `flushend.sty`, `stfloats.sty` |
| `https://mirrors.ctan.org/macros/latex/contrib/changepage.zip` | `2bc8fe362700dd9000a1b06ef2f168f786dca5b78363083ce86c30535f8471b2` | `chngpage.sty` |

Generated style hashes are:

- `flushend.sty`: `fe3d9ad101ade844fd238c6d6b21c9b6935965f81851d3ed6466f687de14226b`
- `stfloats.sty`: `c7103528ae9965d61de38876dfe8a75c6724cab6e14120cd389304ce0d1e1abb`
- `chngpage.sty`: `1cf50d39034d6b0fc8be0cbd9621e64b2e06c9e593887de7d15235dbc0a7501c`

The minimal TeX Live Helvetica and Courier font assets required by the class were vendored from read-only font archives after member inspection:

- `helvetic.tar.xz`: `155b23ee6096e32fe7a481500a75269027042abebc3955e7966327c1d1f41db4`
- `courier.tar.xz`: `eaecb5bcd119e6409ac549fdffbe73a6bf7087daef43085104a1ba03787ec989`

These assets are build dependencies, not research evidence. Their upstream licenses and redistribution terms require accountable-human package review before any public release of a source bundle.
