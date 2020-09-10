# coding: UTF-8

import boto3
import json
import logging
import requests
import os
import re

SLACK_TOKEN = os.environ['slackToken']
GITHUB_TOKEN = os.environ['githubToken']

GITHUB_BASE_URL = "https://api.github.com/repos/getgamba/gamba"
GITHUB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Content-Type': 'application/json',
    'Authorization': "token {0}". format(GITHUB_TOKEN)
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def github_create_pull_req(branch, target):
    payload = {
        'title': 'deployment {0} to {1}'.format(branch, target),
        'head': branch,
        'base': 'deployment/{0}'.format(target)
    }
    response = requests.post("{0}/pulls".format(GITHUB_BASE_URL), headers=GITHUB_HEADERS, data=json.dumps(payload))
    return response.json() if response.ok else None

def github_merge_pull_req(number):
    response = requests.put("{0}/pulls/{1}/merge".format(GITHUB_BASE_URL, number), headers=GITHUB_HEADERS)
    return response.json() if response.ok else None

def lambda_handler(event, context):
    params = parse_qs(event['body'])
    token = params['token'][0]
    if token != SLACK_TOKEN:
        return None

    response_url = params['response_url'][0]
    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params['text'][0] if 'text' in params else ''

    match = re.search(r"([-_.+0-9a-zA-Z]*) *to +(production|staging|app|android|ios|codepush)", command_text)
    if match:
        branch = match.groups()[0] if len(match.groups()[0]) > 0 else 'master'
        target = match.groups()[1]

        res_create = github_create_pull_req(branch, target)
        if res_create and 'number' in res_create:
            res_merge = github_merge_pull_req(res_create['number'])

        return {
            "response_type": "in_channel",
            "text": "これから{0}を{1}にデプロイしまーす！(๑˃̵ᴗ˂̵) \nhttps://circleci.com/gh/getgamba/gamba\nお疲れ様でしたー＼(^o^)／".format(branch, target)
        }

    return {
        "text": "意味わかんなーい(≧∀≦)\n/deploy [<branch_name>] to <production|staging|ios|android|app|codepush>\nこんな感じで話しかけてねー♡",
    }
