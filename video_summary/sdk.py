import requests
import os
import json
import time
import mimetypes


class VideoSummarySDK:
    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self.base_url = base_url or "https://api.videosummary.io"

    def _post_request(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        response = requests.post(url, headers=headers, json=data)
        if not response.ok:
            raise Exception(f"HTTP error! Status: {response.status_code}")

        return response.json()

    def _poll_for_result(self, file_id):
        poll_endpoint = f"{self.base_url}/v1/auto/file/{file_id}?id={file_id}"
        while True:
            response = requests.get(poll_endpoint, headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            })

            if not response.ok:
                raise Exception(f"HTTP error! Status: {response.status_code}")

            result = response.json()
            if result.get('error'):
                return result
            if result.get('file', {}).get('failed_reason'):
                return {'error': result['file']['failed_reason']}
            if result.get('file', {}).get('complete', False):
                return result

            time.sleep(3)

    def _handle_local_file(self, path):
        if not os.path.exists(path):
            return {'error': 'file does not exist'}

        mime_type, _ = mimetypes.guess_type(path)
        endpoint = f"{self.base_url}/v1/auto/upload/{mime_type}"
        response = requests.get(endpoint, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }).json()

        if 'error' in response:
            return response

        upload_url = response.get('upload', {}).get('upload')
        if not upload_url:
            return {'error': 'upload failed'}

        with open(path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f, headers={
                                           'Content-Type': mime_type})

        if upload_response.status_code != 200:
            return {'error': 'upload failed'}

        return {'url': response.get('upload', {}).get('url')}

    def transcribe(self, url, id=None, callback_url=None):
        data = {'url': url, 'id': id, 'callback': callback_url}
        response = self._post_request("/v1/transcribe", data)
        if 'file' in response and 'transcript' in response['file']:
            return self._poll_for_result(response['file']['id'])
        return response

    # Implement other methods (chapter, summarize_and_chapter, summarize) similarly

# Helper function to determine the type of a given URL


def get_url_type(url):
    if url.startswith('http://') or url.startswith('https://'):
        return 'url'
    elif os.path.isfile(url):
        return 'file'
    else:
        return 'path'
