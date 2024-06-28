import asyncio
import json
import httpx
import sys


BOT_ID = ''
USER = ''
AUTH = ''


async def fetch_and_process_stream(query):
    url = 'https://api.coze.com/open_api/v2/chat'
    headers = {
        'Authorization': AUTH,
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }
    data = {
        'bot_id': BOT_ID,
        'user': USER,
        'query': query,
        'stream': True
    }

    try:
        async with httpx.AsyncClient(headers=headers) as client:
            async with client.stream('POST', url, json=data) as response:
                async for chunk in response.aiter_lines():
                    if chunk:
                        if msg := json.loads(
                                chunk.strip('data:')).get('message'):
                            if msg['type'] == 'answer':
                                sys.stdout.write(msg['content'])
                                sys.stdout.flush()
    except httpx.HTTPError as e:
        print(f'HTTP error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')


def main():
    print('Start your query: ')
    while True:
        query = input('\n=> ')
        if query.lower() == 'exit':
            print('Exiting...')
            break
        asyncio.run(fetch_and_process_stream(query))


if __name__ == '__main__':
    main()
