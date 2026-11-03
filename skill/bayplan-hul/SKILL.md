---
name: bayplan-hul
description: "Bayplan HUL" for a vessel bayplan file (fixed-width .asc, e.g. KHS1_2612S_KRUSN_SWIC.asc, container lines like "150082 HALU2500578 HAS     PUSBKK           RF20135F   -250C"). Keeps only the HUL containers — agent HAL / HAC / HAS changed to HUL — for the ports the user chooses (LCH, BKK, or both); every other agent (SKR, KMD, EMC …) and every other port (SGN …) is cut. On kept RF (reefer) containers the temperature loses one digit (-250C -> -25C). The header lines and everything from "***Refer to the following remark." (remark, IMDG, VGM) stay unchanged. Writes output/<name>_HUL_<PORTS>.asc (e.g. KHS1_2612S_KRUSN_SWIC_HUL_BKK-LCH.asc). Use whenever the user says "bayplan", "bayplan HUL", "เก็บตู้ HUL", "ตัด agent อื่น", "HAS เป็น HUL", "ลด TEMP RF", or points to a folder with input/ holding a bayplan .asc.
---

# Bayplan HUL (เก็บตู้ HUL ของ LCH / BKK → output/<name>_HUL_<PORTS>.asc)

Rattana's confirmed format. Run the bundled script; don't edit the file by hand. The file is
fixed-width (198 chars), latin-1 and CRLF. Never change line lengths or line endings.

Web version (same rules): <https://rattanao.github.io/Bayplan/> · repo
<https://github.com/Rattanao/Bayplan>.

## File layout

```
$604    /   /2612S  /…/RECORD=0860/…                 ← header, kept as-is
$600PORT ROTATION/KANPUSUSNSGNLCHBKKLCHSGN           ← header, kept as-is
150082 HALU2500578 HAS     PUSBKK           RF20135F   -250C   13500 …   ← container line
***Refer to the following remark.                    ← from here to the end: kept as-is
***Refer to the following IMDG.
0001003 12190          2 …
***Refer to the following VGM remark.
```

Container line columns (1-based): bay 1-6 · container 8-18 · **agent 20-22** · POL+POD 28-33
(**port = 31-33**, e.g. PUS**BKK**) · type code 45-52 (`RF20135F`) · **temperature from col 56**.

## Rules (confirmed by Rattana)

- Keep a container line only when its agent is **HAL, HAC, HAS or HUL** *and* its port is one
  the user chose (**LCH**, **BKK**, or both; default both). Change the agent to **HUL**.
  Nothing else on the line changes, e.g.
  `250484 SKLU0521628 HUL     PUSLCH           DC20060F                            06000 …`
- **Every other agent is cut** (SKR, KMD, EMC …). **Every other port is cut** (SGN …), even for HUL.
- **RF containers**: the temperature loses one digit, padded with a space so the columns stay put:
  `RF20135F   -250C  ` → `RF20135F   -25C   `, `50C` → `5C`, `210C` → `21C`.
- **Keep unchanged**: the `$604` / `$600` header lines (including `RECORD=0860`, which is not
  recounted), and every line from `***Refer to the following remark.` to the end
  (remark, IMDG, VGM remark).
- Output name = source name + `_HUL_` + chosen ports sorted, joined by `-`
  (`KHS1_2612S_KRUSN_SWIC.asc` → `KHS1_2612S_KRUSN_SWIC_HUL_BKK-LCH.asc`), in `output/`.
- Bytes and CRLF are copied as-is. The source file is never modified.

Checked on KHS1_2612S: 860 containers → 103 kept (LCH 60, BKK 43, matching the CNTRS lists),
757 cut, 1 RF temp changed (HALU2500578 -250C → -25C).

## Input

- A folder with `input/` (or `Input/`) containing **1** `.asc` bayplan file.
- Ports to keep: LCH, BKK or both. Not said = both.

## Steps

1. Run:
   ```bash
   PYTHONIOENCODING=utf-8 python "<skill dir>/scripts/bayplan_hul.py" "<folder containing input>" --ports LCH,BKK
   ```
   (`--ports LCH` or `--ports BKK` for one port only; `--agents` changes the agent list.)
2. Report to the user, in Thai: the job file name, containers total / kept (per port) / cut,
   the RF temps changed, and the output path. If the user sent CNTRS lists for LCH / BKK,
   compare the kept container numbers per port and list any missing or extra.
