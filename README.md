# GEMS Taiwan iGEM 2027 Wiki Template

下一屆 wiki 的起點。頁面、網址、導覽、版型和元件都做好了，內容全部是占位。每一頁的方框寫著評審看什麼，照著填就好。

**線上預覽：<https://timmy97-tw.github.io/GEMS-iGEM-2027-wiki-template/>**（每次 push 到 `main` 由 `.github/workflows/pages.yml` 自動更新）

**這份 repo 是公開的 GitHub template，不是評審看的那份。** 評審只看 iGEM 自己 GitLab 上部署出來的版本，GitHub Pages 預覽和其他網址上的內容都不計分。

## 規則基準：這裡的規則都是 2026 年的

查證日 2026-11-05：iGEM 還沒公布 2027 的規則、日期和網址。下面全部依 2026 版，公布後要重查一次（見「開季第一週」）。

| 規則 | 2026 版內容 | 來源 |
|---|---|---|
| 銅牌 | `/contribution`，加上交 Attributions Form 等交付物 | competition.igem.org/judging/awards/medals |
| 銀牌 | `/engineering`、`/human-practices` | 同上 |
| 金牌 | 自選 3 個 Special Awards（至少各 1 個 General Bio Engineering 與 Specialization），都要達標 | 同上 |
| Special Awards 標準網址 | `/education`、`/entrepreneurship`、`/hardware`、`/inclusivity`、`/human-practices`、`/measurement`、`/model`、`/alternative-platform`、`/safety-and-security`、`/software`、`/sustainability` | judging/awards/special；Judge Handbook p.48 |
| 沒有標準網址的獎 | Best Wiki（看全站）、Best Presentation（看影片）、Part 類獎項（看 Registry）、Village Awards | 同上 |
| Attributions | 從 Deliverables Dashboard 交，**不再要求嵌入 wiki**，公開顯示在隊伍頁 | competition.igem.org/deliverables |
| 頁尾 | 每頁都要有授權聲明和 gitlab.igem.org 的 repo 連結 | 官方 template `layout.html`、`footer.html` |
| 授權 | CC BY 4.0，`LICENSE` 不可修改 | 官方 template README |
| 外部資源 | CSS、JS、字型、圖全部要由 iGEM 提供；圖、字型放 `static.igem.wiki`，影片放 `video.igem.org`；不能用 Google Fonts、jsDelivr、cdnjs | 官方 template README |
| 外部內容 | 不在 wiki、Registry、iGEM GitLab 上的內容，不評分 | Judge Handbook p.29 |
| 大小限制 | 單次 push 11 MiB；部署 artifact 10 MiB | gitlab.igem.org/help/instance_configuration |

**沒有讀到的：** `teams.igem.org/go/deliverables/wiki/requirements` 要登入 iGEM 帳號，這次沒有讀。Communication Policies 全文也沒有讀到。兩份都請 Wiki Lead 登入後核對。

## 五分鐘跑起來

需要 Python 3.8 以上，不用安裝其他東西。

```bash
python3 tools/build.py                       # 依 pages.json 更新導覽和頁尾
python3 -m http.server 8791 --directory site # 然後開 http://localhost:8791
python3 tools/check.py                       # 檢查
```

## 檔案地圖

```
pages.json            全站唯一來源：頁面 ↔ W-ID ↔ 網址 ↔ Drive 資料夾
site/                 會被發布的東西
  index.html          首頁
  <slug>/index.html   每頁一個資料夾，網址就是 /<slug>
  404.html            由 tools/build.py 產生
  assets/css/tokens.css      換主題只改這份
  assets/css/site.css        導覽、版型、頁尾
  assets/css/components.css  元件
  assets/js/                 nav.js、page.js、team.js
  assets/data/site-nav.js    由 tools/build.py 產生，不要手改
  assets/data/roster.js      隊員名單
tools/build.py        更新導覽、頁尾、<title>；補上缺的頁；新增頁
tools/check.py        檢查器
tools/outlines.py     每頁的起始章節和評審重點，只在第一次產生頁面時使用
.gitlab-ci.yml        部署到 iGEM GitLab
LICENSE               CC BY 4.0，不可修改
```

## 頁面清單

24 頁：19 頁是 iGEM 要求（13 個標準網址，加 6 頁官方 template 預設頁），5 頁是 GEMS 每年都寫（Parts、Dry Lab Notebook、Laws and Regulations、Attributions、Milestones）。題目專屬的頁面不在範本裡，定題後再加。

```bash
python3 tools/build.py --list
```

**沒要報的獎項，不要刪那一頁。** 留著，寫一句「本年未選此獎項」，或在 `pages.json` 留著網址。標準網址一改，那個獎就不會被評。檢查器會擋。

## 怎麼寫一頁

1. 看頁面最上方的註解，填上 P 編號。W-ID 不要改。
   ```
   W-ID: W003
   Content owner: P___
   Coding owner: P___
   Cross-checker: P___
   ```
2. 先寫 Drive 的 Master doc，再搬進 HTML。章節標題要和頁面一致。一頁只有一份 Master doc，只有 page owner 改，其他人留言或開 Issue。
3. 把 `<aside class="guide">` 讀完再刪。把占位段落換成內文，**連 `data-ph` 也一起拿掉**，不然檢查器會當成還沒寫。
4. 圖和數字照下面的「元件」做。Hub 的 Figures、Facts「可上線」不是 TRUE，就不能放。
5. 用到外部人物的姓名、照片、引述或 logo，要有 Hub Consent 的 K，狀態是已同意。
6. 跑 `python3 tools/check.py --page W003`。

AI 可以幫忙改句子、排版和除錯，不能產生結果、數據、引用或別人說的話。AI 起草的文字包 `class="ai"`，草稿期會變色，負責的人改寫後再拿掉，並在 Attributions Form 的 AI 欄揭露。官方規定見 `igem.org/legal?tab=ai-policy-teams`。

## 怎麼新增頁面

定題後的題目專屬頁面，用指令加：

```bash
python3 tools/build.py new my-topic --title "My Topic" --tab project --caption "三到五個英文字"
```

`--tab` 可選 `project`、`wetlab`、`drylab`、`engagement`、`team`。這會做完四件事：配下一個 W-ID、寫進 `pages.json`、產生 `site/my-topic/index.html`、更新每頁的導覽和頁尾。

接著你要做兩件事：
1. 在 Hub Pages 開一列，填負責人。
2. 請 Ops 在 `50 Deliverables/Wiki` 開資料夾，名稱照 `pages.json` 的 `drive_folder`。

補充頁一定要從相關的標準頁連過去。評審不會自己找，也不用看。

## 元件

全部直接寫在 HTML 裡，不用框架。範例都在頁面上：DBTL 在 `engineering`，筆記本在 `notebook`，時間軸在 `milestone`，隊員卡在 `team`，利害關係人卡在 `human-practices`，貢獻表在 `attributions`。

**圖（要有 F）。** 檔名 `F0031_W003_TopicA_v02.svg`，先放 Drive `40 Media/Figures/Current`，再用 iGEM 的 uploads tool 傳到 `static.igem.wiki`。編號自動產生。

```html
<figure class="fig" id="F0031" data-fig="F0031" data-page="W003">
  <img src="https://static.igem.wiki/teams/TEAM_ID/wiki/F0031_W003_TopicA_v02.svg" alt="這張圖在說什麼" loading="lazy" />
  <figcaption><span class="fig__label"></span> 圖說，寫 n 和統計方法。 <span class="fig__id">F0031</span></figcaption>
</figure>
<a class="figref" href="#F0031"></a>   <!-- 內文引用，會變成 Figure 1 -->
```

記得拿掉 `fig--pending`，並把 `.fig__slot` 換成 `<img>`。裝飾用的圖不算證據，寫 `<img data-decorative alt="">`。

**數字（要有 V）。** 沒有 V 的數字、人名、引述不進 wiki。

```html
<span class="fact" data-v="V0042">12.3 unit</span>
```

**引用。** 正文寫 `[3]`，會自動連到 `.refs` 列表的第 3 筆，還會加回連。

**貢獻標註。** `<p class="attr"><b>Attribution.</b> Designed by ...</p>`，放在實驗或模型段落結尾。

**DBTL。** 一輪一個 `.cycle`，裡面四格 Design、Build、Test、Learn，下面寫 R、F、V、D。

**筆記本。** 一筆一個 `.nb-entry`，`data-date` 寫日期，`data-run` 寫 R。頁面會自動產生月份篩選和關鍵字搜尋。

**時間軸。** `<ol class="timeline">`，每筆一個 `<li>`，`<time>` 寫真實日期。

**隊員卡。** 改 `site/assets/data/roster.js`，說明在檔案開頭。照片要有 K。

**利害關係人卡。** 一次互動一張 `.ihp-card`，寫 `data-interaction` 和 `data-consent`，沒有 K 只能寫角色。

## 換主題

只改 `site/assets/css/tokens.css` 的 `--brand-*` 和 `--accent`。其他 CSS 有寫死顏色，檢查器會擋。

字型預設用讀者系統內建字型，不用下載。要用隊上的字：上傳到 `static.igem.wiki`，打開 `tokens.css` 開頭那段 `@font-face`，改 `--font-body`。**不要接 Google Fonts。** 中文字型沒切子集會有 10 到 20 MB，請只切用到的字。

KaTeX、three.js 這類函式庫，JS 和 CSS 放進 `site/assets/`，它要的字型傳 `static.igem.wiki`。先算大小，artifact 只有 10 MiB。

## 檢查器

```bash
python3 tools/check.py            # 日常。有 ERROR 才失敗
python3 tools/check.py --page W003
python3 tools/check.py --freeze   # 占位也算失敗。N30 前要跑到全過
```

| 會擋（ERROR） | 會列出（to-do） |
|---|---|
| 少了必要頁面、標準網址被改 | guide 方框還在 |
| `<figure>` 沒 F、沒圖說；`<img>` 不在圖裡 | 內文占位、`[中文方括號]` |
| 數字標了 `.fact` 卻沒有 V | `F____`、`V____` |
| 頁尾少了授權或 repo 連結 | `R____`、`K____` 這類 ID |
| 從 iGEM 以外載入資源 | owner 還是 `P___` |
| 內部連結或資源不存在 | `PROJECT_NAME`、`TEAM_ID` |
| repo 裡有圖、字型、影片 | `draft_marks` 還開著 |
| `tokens.css` 以外有顏色 | 還有 `class="ai"` |
| `site/` 超過 10 MiB | |

GitLab CI 會先跑一次，有 ERROR 就不部署。它只能看結構：看不出數字對不對，也看不出 V 是否真的可上線。那是 Cross-checker 和老師的事。

## 部署到 iGEM GitLab

iGEM 會幫隊伍開好 repo，內容是官方的 Flask template。把它換成這份：

```bash
git clone https://gitlab.igem.org/2027/gems-taiwan.git    # 網址以 iGEM 2027 公告為準
cd gems-taiwan
git rm -r --quiet .                                       # 清掉官方 template
git checkout HEAD -- LICENSE                              # 保留官方 LICENSE，不可修改
# 把這份 template 除了 .git 和 LICENSE 以外的東西全部複製進來
python3 tools/check.py
git add -A && git commit -m "Start the 2027 wiki from the GEMS template"
git push origin main
```

CI 把 `site/` 複製到 `public/`，約 30 秒部署到 `https://2027.igem.wiki/gems-taiwan/`。只有 `main` 會部署。

注意三件事：
- **單次 push 不能超過 11 MiB。** 太大就分批。圖不應該進 repo，所以正常不會碰到。
- **iGEM 平台上要測一次。** 我們沒有 2027 的 repo，這條部署路線還沒在 iGEM 上跑過。開季第一週先推一次空範本，確認 `/contribution`（沒有斜線）打得開、CSS 有載入。
- **網址和隊名改動，只改 `pages.json` 的 `site`。** 改完跑 `python3 tools/build.py`。

**檢查有沒有外部資源：** iGEM 有 External Content Checker（`teams.igem.org/go/deliverables/wiki/har-check`）。Freeze 前每頁跑一次。

## 開季第一週（Wiki Lead）

1. 用「Use this template」開新 repo，放團隊 organization，不放個人帳號。
2. 查 iGEM 2027 公告：標準網址、獎項、頁尾、外部資源、大小限制、日期。有改就更新 `pages.json`、`tools/check.py` 的 `STANDARD`、這份 README。
3. `pages.json` 的 `site` 填 `project_name`、`igem_team_id`。`team_slug`、`wiki_url`、`gitlab_url` 以 iGEM 給的為準。
4. 把 W-ID 和 Master doc 名稱灌進 Hub Pages，填負責人。節點 N14 要求每頁有 owner。
5. 推一次到 GitLab，走完上面的測試。

## 和整套系統怎麼接

| 東西 | 在哪裡 | 誰負責 |
|---|---|---|
| 誰負責哪頁、狀態、未過關數 | Hub `Pages` | Wiki Lead |
| 問題和修正（衝刺期只看這張） | Hub `Issues` | 任何人開，Wiki Lead 排 |
| 圖 | Hub `Figures`，檔案在 `40 Media/Figures/Current` | 圖的作者，Cross-checker 查，老師簽 |
| 數字 | Hub `Facts` | 提出者，Cross-checker 查，老師簽 |
| 文字來源 | `50 Deliverables/Wiki/W### 頁名/W###_頁名_Master` | Content owner |
| 程式 | 這個 repo | Coding owner |

完整的鏈：`R` → `V`、`F` → `W`。**圖不貼進 Word，修正不開新清單，不開個人上傳區。**

相關節點（日期都是占位）：N14 站台與事實 v1、N27 圖定稿、N30 全站最後推送、N31 Freeze。

## 交接給下一屆

Freeze 之後 wiki 就鎖了，這些事要趕在結案（N35）前做：

1. 內容以外的改進（元件、檢查器、頁面指引）帶回這份 template，**不要把當年的專案內容帶回來**：專案名、科學內容、序列、結果、人名、照片、利害關係人、圖都不行。
2. 跑 `python3 tools/check.py`，再用當年的專案名和人名清單 grep 整個 repo，確認沒有殘留。
3. 更新規則基準那張表，寫上查證日。
4. 把 repo 和 Drive 擁有權移交給 Ops，從 Handover Checklist 走一次。
5. 記下當年最難維護的三件事，放進下一屆 Wiki Lead 的交接文。

template 原本是私有的（決議 D-042），2026-11-06 改為公開，好讓 GitHub Pages 能放預覽。要改回私有：`gh repo edit --visibility private --accept-visibility-change-consequences`（免費方案下 Pages 預覽會跟著停掉）。
