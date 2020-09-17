
const request = require('request-promise')
const querystring = require('querystring')

const SLACK_TOKEN = process.env['slackToken']
const GITHUB_TOKEN = process.env['githubToken']

const GITHUB_HOST = "api.github.com"
const GITHUB_PATH = "/repos/getgamba/gamba"
const GITHUB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type': 'application/json',
    'Authorization': `token ${GITHUB_TOKEN}`
}

const GithubAPI = {
    create_pull_req: function(branch, target) {
        const payload = {
            'title': `deployment ${branch} to ${target}`,
            'head': branch,
            'base': `deployment/${target}`
        }
        return request({
            uri: `https://${GITHUB_HOST}${GITHUB_PATH}/pulls`,
            headers: GITHUB_HEADERS,
            method: 'POST',
            json: true,
            body: payload
        })
    },

    merge_pull_req: function(id) {
        return request({
            uri: `https://${GITHUB_HOST}${GITHUB_PATH}/pulls/${id}/merge`,
            headers: GITHUB_HEADERS,
            method: 'PUT',
            json: true,
            body: null
        })
    },
}

exports.handler = function(event, context, callback) {
    context.callbackWaitsForEmptyEventLoop = false
    if (!event['body']) return null

    const params = querystring.parse(event['body'])
    if (params.token != SLACK_TOKEN)
        return null

    const command_text = params['text']
    let match = command_text.match(/([-_.+0-9a-zA-Z]*) *to +(production|staging|app|android|ios|codepush)/)
    if (match) {
        let branch = match[1] || 'master'
        let target = match[2]

        GithubAPI.create_pull_req(branch, target)
            .then((res)=> GithubAPI.merge_pull_req(res.number))
            .catch(()=> undefined)
        return callback(null, {
            response_type: 'in_channel',
            text: `これから${branch}を${target}にデプロイしまーす！(๑˃̵ᴗ˂̵) \nhttps://circleci.com/gh/getgamba/gamba\nお疲れ様でしたー＼(^o^)／`,
        })
    } else {
        callback(null, {
            text: `意味わかんなーい(≧∀≦)\n/deploy [<branch_name>] to <production|staging|ios|android|app|codepush>\nこんな感じで話しかけてねー♡ `
        })
    }
}
