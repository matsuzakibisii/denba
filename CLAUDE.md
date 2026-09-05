# DENBA Health LP — プロジェクトガイド

## 1. 概要

- 内容：DENBA Health のランディングページ＋健康メディア記事サイト（静的HTMLのみ。ビルド・依存パッケージなし）
- 公開URL：https://denba.bisii.co.jp/ （GitHub Pages ＋ `CNAME`）
- リポジトリ：https://github.com/matsuzakibisii/denba.git（`main` ブランチが本番）
- 運営：株式会社BISII／読者ターゲットは40〜70代

## 2. ディレクトリ構成

```
index.html                トップページ（日本語）※約370KB・単一ファイル
en/                       英語版（index / contact-form / disclaimer / tokushoho / media/article-1〜28）
media/
  media.html              記事一覧ページ（全53記事のカード）
  article-N.html          記事本体（N = 1〜53）
  article-N-hero.jpg|png  記事キービジュアル（1〜16は .jpg、17以降は .png）
  chatgpt_articleN_keyvisual_prompt.md  キービジュアル生成用プロンプト
contact-form.html / disclaimer.html / tokushoho.html   問い合わせ・免責・特商法
analytics/                GA4レポート運用（下記7章）
.claude/                  deploy.sh / check-diff.sh（下記3章）
sitemap.xml / robots.txt / favicon.svg / CNAME / google*.html（Search Console確認用）
_gen_avatars.py           アバター画像生成スクリプト
```

ルート直下の `*.jpg`（beef, ichigo, capillary1 など）は index.html で使う説明用画像。

## 3. デプロイ

本番反映は `main` への push（GitHub Pages）。手順は `.claude/` のスクリプトに集約済み。

- `.claude/check-diff.sh` — UserPromptSubmit フック。`origin/main` を pull した上で未コミット差分・未追跡ファイルを要約し、「この内容でデプロイしますか？」の確認を促す
- `.claude/deploy.sh` — 実デプロイ。stash → pull --rebase → `git add -A` → `deploy: update files <YYYY-MM-DD HH:MM:SS>` でコミット → `origin main` へ push

**ルール**

- デプロイは原則 `deploy.sh` を使う（コミットメッセージ形式を揃えるため）。手動コミットする場合も同じ形式に合わせる
- `git add -A` で全差分を巻き込むので、実行前に必ず `git status` を提示してユーザーの承認を得る
- `deploy/YYYYMMDD-HHMMSS` という古いブランチが残っているが現在は未使用。作業対象は `main` のみ
- フォルダ名・パスを変更する場合は `.git` フォルダごと移動する（リモート接続・履歴が保持される）

## 4. 記事追加ワークフロー

新記事を `article-N.html`（N = 既存最大＋1）として追加する際は、以下をすべて更新する。

1. **`media/article-N.html` を作成** — 直近の記事（例：article-53.html）をテンプレートとしてコピーし、以下を必ず差し替える
   - `<title>` / `<meta name="description">`（末尾は `| 健康メディア`）
   - `canonical` と `hreflang`（ja / en / x-default）の各URL
   - OGP・Twitter Card（`og:image` は `https://denba.bisii.co.jp/media/article-N-hero.png`、1280×720）
   - JSON-LD（`BlogPosting`：headline / description / image / url / datePublished / dateModified / mainEntityOfPage）
   - GA4タグ `G-CCCN9E7G60` は**必ず残す**（後述6章）
2. **`media/chatgpt_articleN_keyvisual_prompt.md` を作成** — 5章参照
3. **`media/media.html`** の一覧先頭に記事カードを追加
4. **`index.html`** の記事カード枠（先頭1枚が最新記事）を新記事に差し替え
5. **`sitemap.xml`** に `<loc>https://denba.bisii.co.jp/media/article-N.html</loc>` を追加（`lastmod` = 公開日、`changefreq` monthly、`priority` 0.6）。既存記事を更新した場合は該当 `lastmod` も更新
6. 差分を確認して `deploy.sh` でデプロイ

**記事の書き方の型**：タイトルは「〜は思い込み？」という切り口＋テーマ。本文は40〜70代向けに、断定的な医療効果を謳わない穏やかなトーン。配色は `--gold:#B8985A` `--sage:#C7A957` `--ink:#1E1E1E` `--parch:#F0EBE0`、和文フォントは Noto Sans JP / Noto Serif JP。CSSは各HTML内に `<style>` で内包（外部CSSファイルは作らない）。

## 5. キービジュアル生成・差し替え

画像生成は ChatGPT 側で行うため、Claude は**プロンプトを書き、生成後にHTMLへ差し替える**役割。

- `media/chatgpt_articleN_keyvisual_prompt.md` に、共通指示（実写フォトリアル・16:9・ゴールド／セージ／生成りの色味・人物の顔は写さない・ロゴやブランド不可・明朝体でタイトルを配置）と、そのままコピーできるプロンプト本文を書く
- **直近数記事と構図が被らないこと**を必ずプロンプト内で明示する（舞台・時間帯・被写体を変える）
- ユーザーが `media/article-N-hero.png` として保存し「差し替え」と伝えたら、article-N.html・media.html・index.html の画像参照を差し替える

## 6. SEO・計測のルール

- **GA4タグ（`G-CCCN9E7G60`）を削除しない。** Search Console の所有権確認が Google Analytics 経由のため、タグを消すと確認が外れる
- 全ページに canonical / hreflang（ja・en・x-default）／OGP／JSON-LD を入れる
- `robots.txt` は全許可＋ `Sitemap: https://denba.bisii.co.jp/sitemap.xml`
- Search Console は URLプレフィックスプロパティ `https://denba.bisii.co.jp/`。記事の未インデックス対策としてサイトマップ送信済み
- 英語版 `en/` は article-1〜28 までしか存在しない。日本語記事の `hreflang="en"` は未作成ページを指す場合があるため、英語版を追加する際はここから埋める

## 7. アナリティクス運用（`analytics/`）

- `ga-daily-log.csv` — GA4日次指標の追記ログ（date / active_users / new_users / sessions / key_events / チャネル別セッション / top_page / avg_engagement_time）。**過去行は書き換えない**（GA側の確定処理で数値が後日ずれるが、行内の整合性を優先し、ずれは週次集計で織り込む）
- `reports/daily/YYYY-MM-DD.md` — 日次レポート。主要指標（前日比）／チャネル別／上位ページ／数値から言えること・改善案／データ品質メモ の構成
- `reports/weekly/YYYY-Www.md`・`reports/monthly/` — 週次・月次サマリー
- `denba-acquisition-action-plan.md` — 広告以外の集客アクションプラン（AEO強化・内部リンク・被リンク獲得・SNS・メール／LINE）。月次サマリーのタイミングで優先度を見直す

**分析時の注意**：日次の母数が1桁〜十数のため、海外からの自動巡回（米国・ポーランド等でエンゲージメント0%）が混じると数字が大きく歪む。全体値と「日本のみの実質値」を併記して評価する。

## 8. 既知の未整備事項

- キービジュアル未生成：article-48・50〜53（HTMLは画像を参照しているが実ファイルなし）
- `article-46-hero.png` / `article-47-hero.png` がプロジェクトルートに置かれたまま（本来は `media/` 配下）
- キーイベント（問い合わせフォーム送信）がGA4で全期間ゼロ。計測設定の確認が必要
- `.claude/check-diff.sh.bak` は旧版のバックアップ（未使用）
