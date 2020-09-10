
# AWS Lambda Slack CircleCI Deploy Bot

A Slack bot for AWS Lambda that automate deployment with Circle CI.

## Install

### Slackの設定
1. Slashのワークスペース管理より、Appカスタムインテグレーションへ進み、Slash Commandsを追加します。
1. Slash Commandsのインテグレーションを追加し、トークンに表示された内容を取得します。

### AWS Lambdaの準備
1. AWS Lambdaに用意されているBluePrintに用意されている、`Slack-echo-command`を元に、lambda関数を作成します。
1. 以下のコマンドにより、`lambda_function.zip`を作成します
    ```
    $ ./deploy.sh
    ```
1. AWS Lambdaの関数コードに`lambda_function.zip`をアップロードします
1. 以下の2つの環境変数を登録します
    * `githubToken`: Githubのアクセストークン
    * `slackToken`: Slackの設定で表示されたトークン

### API Gatewayの設定
1.  `/gamba_deploy_bot - ANY - 統合リクエスト`を開き、マッピングテンプレートを追加します
    * Content-TYpe: `application/x-www-form-urlencoded`
    * テンプレート: `{ "body": $input.json("$") }`
2. APIをデプロイします
3. このとき表示されたURLをメモします

### Slackの設定(続き)
1. API Gatewayで取得したURLをSlash CommandsのURLに設定します
1. ユーザの名前には`deploy_bot`、アイコンには適切な画像を設定します

## Usage
Slackのチャネルに対して、以下のコマンドを送ると、デプロイが始まります。

```
/deploy branch_name to environment
```
* `branch_name`: デプロイするブランチ名を指定します。省略時は`master`がはいります。
* `environment`: 以下のいずれかを指定します。
  * `production`: 本番環境
  * `staging`: ステージング環境
  * `app`: iOS/Androidのアプリのビルド＆AppStore/GooglePlayへのアップロード
  * `android`: Androidのアプリのビルド＆GooglePlayへのアップロード 
  * `ios`: iOSのアプリのビルド＆AppStoreへのアップロード 
  * `codepush`: CodePushへのJSコードのアップロード

