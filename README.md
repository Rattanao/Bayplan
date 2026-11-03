# BAYPLAN — เก็บตู้ HUL (LCH / BKK)

เก็บเฉพาะตู้ของ HUL จากไฟล์ Bayplan (.asc เช่น `KHS1_2612S_KRUSN_SWIC.asc`) ตามท่าที่เลือก

## สิ่งที่โปรแกรมทำ

- เอเย่นต์ **HAL / HAC / HAS** → **HUL** (เฉพาะตำแหน่งเอเย่นต์ ส่วนอื่นของบรรทัดคงเดิมทุกตัวอักษร)
- เลือก HUL ที่จะเก็บ: **LCH**, **BKK** หรือทั้งสองท่า
- **Agent อื่น เช่น SKR, KMD, EMC ตัดทิ้งเสมอ** · ท่าอื่น เช่น SGN ตัดทิ้งเสมอ
- ตู้ **RF** ลด TEMP 1 ตำแหน่ง: `RF20135F   -250C` → `RF20135F   -25C` (เติมช่องว่าง คอลัมน์อื่นไม่เลื่อน)
- บรรทัดหัวไฟล์ `$604` / `$600` คงเดิม
- ตั้งแต่บรรทัด `***Refer to the following remark.` / `***Refer to the following IMDG.` จนจบไฟล์ คงเดิม
- ชื่อไฟล์ที่ได้ = ชื่อต้นฉบับ + `_HUL_` + ท่า เช่น `KHS1_2612S_KRUSN_SWIC_HUL_BKK-LCH.asc`
- ไบต์และการขึ้นบรรทัด (CRLF) คงเดิม ไฟล์ต้นฉบับไม่ถูกแก้ไข

## วิธีใช้ 1: หน้าเว็บ

เปิด <https://rattanao.github.io/Bayplan/> (หรือ `index.html`) → ลากไฟล์ .asc มาวาง → ติ๊ก LCH / BKK →
ตรวจตัวเลขสรุปและไฮไลต์ → กด **บันทึกไฟล์** · กด **เคลียร์ข้อมูล** เพื่อเริ่มงานใหม่ ·
ประมวลผลในเบราว์เซอร์ ไม่มีการอัปโหลดไฟล์

## วิธีใช้ 2: คำสั่ง Python

```
12-Bayplan/
├─ bayplan_hul.py
├─ input/    ← วางไฟล์ .asc 1 ไฟล์
└─ output/   ← ได้ <ชื่อไฟล์>_HUL_BKK-LCH.asc ที่นี่
```

```bash
python bayplan_hul.py . --ports LCH,BKK
```

## วิธีใช้ 3: skill ของ Claude

พิมพ์ `bayplan HUL เก็บ LCH BKK` ไฟล์ skill อยู่ที่ `skill/bayplan-hul/SKILL.md`
