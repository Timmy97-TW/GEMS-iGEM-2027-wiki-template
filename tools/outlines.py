# -*- coding: utf-8 -*-
"""Seed outline of every page: section headings, what judges look for, and which
placeholders the section starts with. tools/build.py reads this only to scaffold
a page that does not exist yet. Once a team member owns a page, the page file is
the truth and this file is no longer used for it.

Sources for the guidance, all read 2026-11-05 and all 2026 rules (2027 rules are
not published): iGEM Medals and Special Awards pages (ballot questions), and the
2026 Judge Handbook. Guidance is paraphrased, written in Traditional Chinese for
the students. Headings are English because judges read the wiki in English.

Each section: (heading, guide, options)
  options: figs = list of figure hints, facts = list of fact hints,
           block = name of a component block in tools/build.py, attr = True for
           an attribution line
"""

SHARED_ABSTRACT = "用 3 到 5 句寫：這頁要說服評審什麼、最重要的證據是什麼。評審從評分表直接連到這頁，不會先讀別頁。"

OUTLINES = {
"home": {
  "lede": "[一句話說清楚專案解決什麼問題，以及怎麼解決。]",
  "kicker": "GEMS Taiwan · iGEM 2027",
  "sections": [
    ("The problem", "Best Wiki 評審先問：網站有沒有把專案和目標講清楚。首頁第一屏就要讓陌生人知道問題是什麼、誰受影響。問題的數字要有 V。", {"facts": ["問題規模的數字"], "figs": ["問題示意圖"]}),
    ("Our approach", "用一張系統圖講完做法，不要堆術語。評審要的是「看完知道你們做了什麼」。", {"figs": ["系統總覽圖"]}),
    ("What we achieved", "只放已驗證的成果，每項連到證明它的頁面。沒做到的不要寫成做到了。", {"facts": ["最重要的一個成果數字"]}),
    ("Explore the wiki", "幫評審找到內容是 Best Wiki 的評分項目。保留這些入口，或換成更好的導覽，但要連到標準頁面。", {"block": "doors"}),
  ]},
"description": {
  "lede": "[專案為什麼值得做：問題、現有做法的缺口、我們的答案。]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("The problem", "說明問題和受影響的人，引用文獻。背景是為了讓評審理解你們的選擇，不是教科書。", {"facts": ["問題規模的數字"], "figs": ["問題示意圖"]}),
    ("Why existing approaches fall short", "評審會問你們有沒有認真看過前人的做法。列出現有方案與缺口，含過去 iGEM 隊伍，並標明出處。", {}),
    ("Our solution", "講清楚系統如何運作、每個模組做什麼。圖和文字要對得起實驗頁，不要比實驗頁說得更滿。", {"figs": ["系統運作圖"]}),
    ("How the work evolved", "連到 Human Practices 與 Engineering，說明想法如何因證據或利害關係人而改變。", {}),
  ]},
"engineering": {
  "lede": "[我們如何用 Design、Build、Test、Learn 把問題逐步解決。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Engineering goals", "銀牌要求至少跑完一輪設計循環。手冊把失敗和成功看得一樣有價值，重點是假設被驗證或被推翻。先寫每個目標的假設與成功標準。", {"facts": ["成功標準的數值"]}),
    ("Cycles", "每一輪都要有 Design、Build、Test、Learn，而且 Learn 要實際改變下一輪的 Design。用了 Part 來達標時，文件必須放在 Registry 的 Part 頁面。多輪都放這裡；每張結果圖有 F，每個數字有 V 並連回 R。", {"block": "dbtl", "attr": True}),
    ("What we would do next", "評審要看你們知道下一輪會改什麼，以及為什麼。", {}),
  ]},
"contribution": {
  "lede": "[我們留給未來 iGEM 隊伍的東西，以及他們要怎麼用。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Contributions at a glance", "銅牌必備。一定要明寫「為什麼這對其他隊伍有用」。形式不限，可以是資料、工具、Part 文件或除錯紀錄。", {}),
    ("Contribution details", "每項一小節：是什麼、怎麼重現、驗證到什麼程度、限制。用既有 Part 達標時，文件要加在 Registry 該 Part 上，這裡放連結。", {"figs": ["貢獻成果或使用方式"], "facts": ["可重用的規格或數據"]}),
    ("How future teams can use this", "寫給下一屆的學生看：從哪開始、要準備什麼、會在哪裡卡住。", {}),
  ]},
"results": {
  "lede": "[實際做到什麼，有什麼證據，還有什麼沒做到。]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Key results", "Best Wiki 評審問：結果有沒有令人信服的實驗證據。每個主張對應一張圖和一組數字；圖說寫 n、統計方法與對照組。", {"figs": ["主要結果圖"], "facts": ["主要結果數值（含單位與 n）"], "attr": True}),
    ("Proof of concept", "評審會把目標和結果對照。清楚說明系統到哪一步被驗證，哪些是模型推估，哪些是實驗。", {"figs": ["概念驗證"]}),
    ("What did not work", "手冊明說失敗也有價值。誠實寫出沒成功的部分與你們的判斷，比隱瞞更有分數。", {}),
    ("Future work", "下一步要做什麼、需要什麼才做得到。", {}),
  ]},
"alternative-platform": {
  "lede": "[選擇這個非典型平台的理由，以及如何在其上完成工程。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Why this platform", "此獎項涵蓋常見模式生物以外的平台。評審問：平台是否真的適合要解決的問題，以及成果和平台綁得多緊。這一年不參賽就把這頁寫明「本年未選此獎項」，不要刪除網址。", {}),
    ("Engineering evidence", "評審問：成功工程化的證據有多強。放資料，不放願景。", {"figs": ["工程化證據"], "facts": ["關鍵結果數值"]}),
    ("What did not work", "評審明確要看什麼沒成功、為什麼、其他人該注意什麼。", {}),
    ("Safety on this platform", "連到 Safety and Security；高中隊伍要在 iGEM White List 內，不確定就先問 safety@igem.org。", {}),
  ]},
"experiments": {
  "lede": "[我們怎麼做實驗，讓別人可以照著重做。]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Experimental overview", "按目標而不是按日期組織。每個目標連到對應結果與 Engineering 的循環。", {"figs": ["實驗流程總覽"]}),
    ("Protocols", "寫到別的隊伍能重做：材料、條件、對照組。內容來自 Hub SOPs 的現行版，寫 S 編號與版本，不另外寫一份。", {"facts": ["關鍵實驗條件"], "attr": True}),
    ("Controls and validation", "說明你怎麼知道實驗本身是可信的。", {}),
  ]},
"measurement": {
  "lede": "[我們量什麼、怎麼校正，別的隊伍能否重現。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("What we measured and why", "手冊：選對要量的東西，比量得多重要。定性結果要說明如何走向定量；寧可承認只有定性，也不要報有問題的定量數字。", {"facts": ["量測目標與單位"]}),
    ("Methods and protocols", "評審問：方法描述得夠不夠好，其他隊伍能否重現。", {"figs": ["量測方法"]}),
    ("Calibration and validation", "評審問：有沒有適當校正與驗證。放校正曲線、標準品、誤差來源。", {"figs": ["校正曲線"], "facts": ["校正結果"]}),
    ("Usefulness to other projects", "評審問：這套量測對別的專案有沒有用。寫清楚誰能用、怎麼用。", {}),
  ]},
"safety-and-security": {
  "lede": "[我們怎麼辨識和管理風險，也對領域的安全做了什麼。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Lab safety and risk assessment", "手冊要求所有隊伍管理對自己、同伴、社區與環境的風險。內容直接引用 Safety Register，不要為 wiki 另寫一份。高中隊伍必須在 White List 內。", {"attr": True}),
    ("Safety forms", "寫明交了哪些表、何時交。表單本身可在隊伍頁面公開查閱。", {}),
    ("Project-specific risks", "評審問：有沒有妥善管理本專案的風險。說明生物安全與生物保全各自怎麼處理。", {}),
    ("Contribution to safety", "參賽獎項才需要。評審問：對生物安全或保全有什麼貢獻、驗證到什麼程度、是否建立在既有知識上、有沒有考慮真實世界的使用。", {"figs": ["安全措施或驗證"]}),
  ]},
"notebook": {
  "lede": "[濕實驗的日常紀錄：哪天做什麼、結果怎麼樣、對應哪個 Run。]",
  "sections": [
    ("How to read this notebook", "評審用這頁確認工作真的做過。每筆對應 Hub Runs 的一個 R，內容從 Run Record 來，不另外重打。", {}),
    ("Entries", "按時間排，一個 Run 一筆，可依月份或關鍵字篩選。避免貼未整理的原始檔。", {"block": "notebook"}),
  ]},
"parts": {
  "lede": "[我們的 Part，以及 Registry 文件在哪裡。]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Parts table", "Part 獎項沒有標準頁面，評審只看 Registry。這頁只當索引，每列連到 Registry，並寫 C 編號。內容要先寫進 Registry，不是寫在這裡。", {"block": "parts"}),
    ("Collections", "有 Part Collection 才保留。評審問：這是一組為了共同運作而設計的 Part，還是只是列出所有做過的 Part。", {}),
    ("Characterization", "摘要最重要的特性資料，連到 Results 與 Measurement，不要重複貼圖。", {"figs": ["Part 特性資料"], "facts": ["關鍵特性數值"]}),
  ]},
"model": {
  "lede": "[模型回答了什麼問題，以及它如何改變我們的設計。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Questions the model answers", "評審問：模型是否幫隊伍理解、預測或設計。先寫模型要回答的問題，再寫方程式。", {}),
    ("Model design and assumptions", "寫出假設與參數來源；每個參數一個 V，連回 R 或文獻。程式放團隊 repo，寫 commit。", {"figs": ["模型結構圖"], "facts": ["模型參數與來源"], "attr": True}),
    ("Validation", "評審問：有沒有用實驗或其他相關資料來開發、訓練或驗證。沒驗證到的要明說。", {"figs": ["模型與實驗比較"]}),
    ("How the model changed the project", "具體寫哪個決定因模型而改變，連到 Engineering 的循環。評審問這能否成為他人的範例。", {}),
  ]},
"hardware": {
  "lede": "[這個硬體解決合成生物學的什麼需求，別人能否做出來。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("The need", "評審問：硬體是否針對合成生物學的需求或問題。", {}),
    ("Design and build", "每個裝置用 H 專案編號對應。CAD 與韌體放團隊 repo，圖放 static.igem.wiki。檔案若太大，只放下載連結到 iGEM 平台。", {"figs": ["裝置設計圖"], "facts": ["關鍵規格"], "attr": True}),
    ("Proof of concept", "評審問：有沒有展示實用性與功能性。", {"figs": ["功能測試結果"]}),
    ("User testing", "評審問：有沒有做使用者測試，並從回饋中學到東西。對象的姓名與照片要有 K。", {}),
    ("Reproducibility", "評審問：文件足不足以讓其他隊伍重做。列出零件清單、組裝步驟、成本。", {"facts": ["成本與零件數"]}),
  ]},
"software": {
  "lede": "[這個工具做什麼、誰能用、怎麼安裝。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("What the tool does", "評審問：工具能否對其他專案有用。不必大或複雜，但要解決真實問題。", {"figs": ["工具畫面或流程"]}),
    ("Install and use", "評審問：是否好用。一定要 OSI 核可授權，原始碼放 iGEM GitLab 的專用 repository，這裡放連結；2026 起最多可交 5 個 repository。", {}),
    ("Validation", "評審問：用實驗、測試資料或基準比較驗證到什麼程度。", {"facts": ["驗證結果"], "attr": True}),
    ("Standards and integration", "評審問：是否相容於合成生物學標準（例如 SBOL），能否與外部工具整合（API、套件）。", {}),
    ("Documentation for developers", "評審問：程式與文件是否方便未來隊伍擴充。", {}),
  ]},
"drylab-notebook": {
  "lede": "[運算與硬體工作的日常紀錄：跑了什麼、結果如何、對應哪個 Run。]",
  "sections": [
    ("How to read this notebook", "評審用這頁確認工作真的做過。以 Hub Runs 為準：一次運算或測試一個 R，這頁只是它的發布版。", {}),
    ("Entries", "按時間排，一個 Run 一筆，附 commit 與輸出檔位置。", {"block": "notebook"}),
  ]},
"human-practices": {
  "lede": "[我們如何判斷專案負責任且對世界有益，以及外界如何改變了專案。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Values and framework", "銀牌問：設計時放了哪些價值、諮詢了誰、有什麼證據說明專案負責任且有益。寫出你們的框架和理由。", {}),
    ("Project evolution", "評審問：HP 工作是否融入整個專案。畫出每個改變：互動 I、決議 D、專案怎麼變。", {"figs": ["專案演變圖"]}),
    ("Stakeholder engagement", "評審問：是否納入不同立場的利害關係人，說清脈絡與理由。每個人一張卡，沒有同意紀錄 K 就不放姓名、照片、引述和 logo。對象未成年時另需校方或家長許可。", {"block": "ihp"}),
    ("Implementation and end users", "銀牌問：誰會用、怎麼用、真實世界怎麼落地、有什麼影響。", {}),
    ("What others can build on", "評審問：文件是否能讓他人接續，並成為激勵他人的範例。", {}),
  ]},
"education": {
  "lede": "[我們和誰對話、彼此學到什麼。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Who we reached and why", "此獎看的是雙向對話。評審問：有多促進相互學習或對話。不是推銷 iGEM 或合成生物學。活動不一定要跟專案相關。", {"facts": ["場次與參與人數"]}),
    ("Activities", "評審問：是否經過思考地執行。每場活動一張卡，對應 Interactions 的 I。未成年參與者不寫姓名，照片要有校方或家長許可（K）。", {"block": "ihp", "figs": ["活動紀錄"]}),
    ("What participants and we learned", "放真實回饋與改了什麼。評審問：有沒有讓更多人能參與合成生物學。", {"facts": ["回饋資料"]}),
    ("Materials others can reuse", "評審問：文件是否能讓他人接續。附教材與使用說明。", {}),
  ]},
"entrepreneurship": {
  "lede": "[這個專案如何成為真實的產品或事業。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Customers and unmet need", "評審問：是否找到第一批潛在客戶，以及現有方案沒解決的需求。要有訪談證據，對象姓名要有 K。", {"facts": ["市場或需求數字"]}),
    ("Solution and feasibility", "評審問：方案是否可行、可放大、具創新性。此獎項也期待最小可行產品。", {"figs": ["產品或原型"]}),
    ("Development plan", "評審問：是否有合理的里程碑、時程、資源與風險。", {"figs": ["產品開發路線圖"]}),
    ("Team and partners", "評審問：為了可信地發展下去需要哪些能力與合作者。", {}),
    ("Long-term impact", "評審問：是否考慮完整方案的長期正負面影響。", {}),
  ]},
"sustainability": {
  "lede": "[我們選了哪些 SDG、如何評估，以及實際造成什麼改變。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Chosen goals and evaluation", "評審問：工作是否可衡量且顯著地處理了一個或多個 SDG。選少數幾個，寫明為什麼與如何評估。", {"facts": ["SDG 相關指標"]}),
    ("Stakeholder feedback", "評審問：有沒有把相關利害關係人的回饋納入工作。", {}),
    ("Long-term impacts and interactions", "評審問：長期的社會、環境與經濟影響，以及對其他 SDG 的正負面作用。", {"figs": ["影響評估"]}),
    ("What others can build on", "評審問：SDG 的工作是否記錄得讓其他隊伍能接續。", {}),
  ]},
"inclusivity": {
  "lede": "[我們辨識了哪些參與障礙，並如何降低它們。]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Barriers we investigated", "評審問：多深入調查了參與科學的障礙。活動不一定要跟專案相關。", {"facts": ["障礙的調查數據"]}),
    ("What we did", "評審問：有多擴大了接觸合成生物學或科學的機會。", {"figs": ["活動或成果"]}),
    ("Dialogue with the group", "評審問：有沒有和目標族群對話，並考慮他們的需要、意見與價值。", {}),
    ("What others can build on", "評審問：文件是否能讓其他隊伍或外部單位接續。", {}),
  ]},
"laws-and-regulations": {
  "lede": "[專案落地會碰到的法規，以及我們如何因此調整。]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Regulatory landscape", "不是標準頁面，但可從 Human Practices 連過來當補充資料。內容要連回法規原文，並寫明查閱日期。", {"facts": ["法規條文與日期"]}),
    ("What this means for our project", "寫出法規造成的具體設計或計畫改變，連到 Human Practices。", {}),
    ("Expert input", "諮詢對象的姓名、引述、logo 都要有 K。沒有 K 的影像一律不上。", {"block": "ihp"}),
  ]},
"team": {
  "lede": "[我們是誰。]",
  "sections": [
    ("Members", "2026 起 Attributions 資料直接顯示在 iGEM 隊伍頁。名單從 Hub Roster 抄公開欄到 assets/data/roster.js，肖像要有 K。", {"block": "team"}),
  ]},
"attributions": {
  "lede": "[誰做了什麼，誰幫了我們。正式紀錄在 iGEM 的 Attributions Form。]",
    "sections": [
    ("Official Attributions Form", "2026 起 Attributions Form 從 Deliverables Dashboard 交，不再要求嵌入 wiki，公開顯示在隊伍頁。銅牌要求每欄都填，包含 specific tasks。評審會比對是否合理。AI 的使用也要在這裡揭露。", {"block": "attribution-link"}),
    ("Who did what", "這張表是 Hub 與 Attribution 表的摘要，只放公開內容。外部協助者要有 K 才能列名。", {"block": "attribution"}),
  ]},
"milestone": {
  "lede": "[這一年怎麼走過來。]",
  "sections": [
    ("Our year", "來自 Milestones Caption，每筆有真實日期。照片每張要連到 M；有可辨識的人要有 K。", {"block": "timeline"}),
  ]},
}
