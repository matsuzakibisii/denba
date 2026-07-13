# DENBA Health LP

## プロジェクト概要
- 内容：DENBA Health のランディングページ・メディア記事サイト
- 公開URL：GitHub Pages（CNAME設定済み、カスタムドメイン運用）
- Gitリポジトリ：https://github.com/matsuzakibisii/denba.git（mainブランチ）

## 構成
- `index.html` — トップページ（日本語）、`en/index.html` — 英語版
- `media/` — 記事一覧（article-1〜22.html）＋各記事のヒーロー画像・DALL-Eプロンプト
- `contact-form.html` / `disclaimer.html` / `tokushoho.html` — 問い合わせ・免責・特商法表記
- `_gen_avatars.py` — アバター画像生成スクリプト
- `.claude/` — カスタムスラッシュコマンド等（既存）

## 作業ルール
- 本番反映はGit push（GitHub Pages経由）のため、変更は必ずコミット・pushする
- 記事追加時はDALL-Eプロンプト（`chatgpt_article*_keyvisual_prompt.md`）の命名規則に合わせる
- フォルダ名・パスを変更する場合は `.git` フォルダごと移動すること（リモート接続・履歴は保持される）
