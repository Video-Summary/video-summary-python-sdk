import requests
import os
import json
import time
import mimetypes


class VideoSummarySDK:
    def __init__(self, api_key, base_url="https://api.videosummary.io"):
        if api_key == 'your_api_key':
            raise ValueError(
                "Invalid API key. Please provide a valid API key.")
        self.api_key = api_key
        self.base_url = base_url

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
            if result.get('file', {}).get('complete', False):
                return result

            time.sleep(3)

    def _handle_file(self, file_path):
        if not os.path.exists(file_path):
            return {'error': 'file does not exist'}

        mime_type, _ = mimetypes.guess_type(file_path)
        # coerce the mime type into one of these ['mp4', 'mp3', 'wav', 'youtube']
        # mime type must be on eof ['mp4', 'mp3', 'wav', 'youtube']. convert it
        if mime_type == 'video/mp4':
            mime_type = 'mp4'
        elif mime_type == 'audio/mp3':
            mime_type = 'mp3'
        elif mime_type == 'audio/wav':
            mime_type = 'wav'

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

        with open(file_path, 'rb') as f:
            upload_response = requests.put(upload_url, data=f, headers={
                                           'Content-Type': mime_type})

        if upload_response.status_code != 200:
            return {'error': 'upload failed'}

        return {'url': response.get('upload', {}).get('url')}

    def transcribe(self, url, id=None, callback_url=None):
        """
        Transcribes the audio content of a video into text. This method can handle both URLs and local file paths.

        Parameters:
        url (str): The URL of the video or the path to a local file.
        id (str, optional): An optional identifier for the transcription task.
        callback_url (str, optional): A callback URL to notify upon completion of the transcription.

        Returns:
        dict: A dictionary containing the transcription ('transcript') and the file ID ('fileId'). 
              If an error occurs, an error message is returned.
        """
        data = {'url': url, 'id': id,
                'callback': callback_url, 'external_url': True}
        # Handle local file path
        if not url.startswith('http://') and not url.startswith('https://'):
            file_result = self._handle_file(url)
            if 'error' in file_result:
                return file_result
            data['external_url'] = False
            data['url'] = file_result['url']

        # if it's a youtube url, we need to add the youtube flag is_youtube: True
        if 'youtube.com' in data['url'] or 'youtu.be' in data['url']:
            data['is_youtube'] = True
        response = self._post_request("/v1/transcribe", data)
        if 'file' in response:
            result = self._poll_for_result(response['file']['id'])
            if 'file' in result and 'transcript_url' in result['file']:
                transcript_url = result['file']['transcript_url']
                transcript_response = requests.get(transcript_url)
                if transcript_response.ok:
                    transcript = transcript_response.json()
                    return {'transcript': transcript, 'fileId': response['file']['id']}
                else:
                    return {'error': 'Failed to fetch transcript'}
            else:
                return {'error': 'Unknown error, transcription failed'}
        return response

    def chapter(self, url, id=None, callback_url=None):
        """
        Extracts chapter information from a video. This method supports both URLs and local files.

        Parameters:
        url (str): The URL of the video or the path to a local file.
        id (str, optional): An optional identifier for the chapter extraction task.
        callback_url (str, optional): A callback URL to notify upon completion.

        Returns:
        dict: A dictionary containing the chapters ('chapters'), transcript ('transcript'), 
              and file ID ('fileId'). If an error occurs, an error message is returned.
        """
        data = {
            'url': url,
            'external_url': True,
            'chapter': True,
            'summarize': False,
            'id': id,
            'callback': callback_url
        }
        # Handle local file path
        if not url.startswith('http://') and not url.startswith('https://'):
            file_result = self._handle_file(url)
            if 'error' in file_result:
                return file_result
            data['external_url'] = False
            data['url'] = file_result['url']

        response = self._post_request("/v1/summary", data)
        if 'file' in response:
            result = self._poll_for_result(response['file']['id'])
            if 'file' in result:
                chapter_response = {}
                if 'transcript_url' in result['file']:
                    transcript_url = result['file']['transcript_url']
                    transcript_response = requests.get(transcript_url)
                    if transcript_response.ok:
                        chapter_response['transcript'] = transcript_response.json(
                        )

                if 'chaptering_url' in result['file']:
                    chaptering_url = result['file']['chaptering_url']
                    chaptering_response = requests.get(chaptering_url)
                    if chaptering_response.ok:
                        chapter_response['chapters'] = chaptering_response.json(
                        )

                chapter_response['fileId'] = response['file']['id']
                return chapter_response
            else:
                return {'error': 'Unknown error, chapter extraction failed'}
        return response

    def summarize(self, url, id=None, callback_url=None):
        """
        Generates a summary of a video's content. This method accepts both URLs and local file paths.

        Parameters:
        url (str): The URL of the video or the path to a local file.
        id (str, optional): An optional identifier for the summarization task.
        callback_url (str, optional): A callback URL to notify upon completion.

        Returns:
        dict: A dictionary with the summary ('summary'), transcript ('transcript'), 
              and file ID ('fileId'). If an error occurs, an error message is returned.
        """
        data = {
            'url': url,
            'external_url': True,
            'chapter': False,
            'summarize': True,
            'id': id,
            'callback': callback_url
        }
        # Handle local file path
        if not url.startswith('http://') and not url.startswith('https://'):
            file_result = self._handle_file(url)
            if 'error' in file_result:
                return file_result
            data['external_url'] = False
            data['url'] = file_result['url']

        response = self._post_request("/v1/summary", data)
        if 'file' in response:
            result = self._poll_for_result(response['file']['id'])
            if 'file' in result:
                summary_response = {}
                if 'transcript_url' in result['file']:
                    transcript_url = result['file']['transcript_url']
                    transcript_response = requests.get(transcript_url)
                    if transcript_response.ok:
                        summary_response['transcript'] = transcript_response.json(
                        )

                if 'final_summary' in result['file']:
                    summary_response['summary'] = result['file']['final_summary']

                summary_response['fileId'] = response['file']['id']
                return summary_response
            else:
                return {'error': 'Unknown error, summarization failed'}
        return response

    def summarize_and_chapter(self, url, id=None, callback_url=None):
        """
        Performs both summarization and chapter extraction on a video. This method handles URLs and local file paths.

        Parameters:
        url (str): The URL of the video or the path to a local file.
        id (str, optional): An optional identifier for the task.
        callback_url (str, optional): A callback URL for completion notification.

        Returns:
        dict: A dictionary containing the chapters ('chapters'), summary ('summary'), transcript ('transcript'), 
              and file ID ('fileId'). If an error occurs, an error message is returned.
        """
        data = {
            'url': url,
            'external_url': True,
            'chapter': True,
            'summarize': True,
            'id': id,
            'callback': callback_url
        }
        # Handle local file path
        if not url.startswith('http://') and not url.startswith('https://'):
            file_result = self._handle_file(url)
            if 'error' in file_result:
                return file_result
            data['external_url'] = False
            data['url'] = file_result['url']

        response = self._post_request("/v1/summary", data)
        if 'file' in response:
            result = self._poll_for_result(response['file']['id'])
            if 'file' in result:
                summary_chapter_response = {}
                if 'transcript_url' in result['file']:
                    transcript_url = result['file']['transcript_url']
                    transcript_response = requests.get(transcript_url)
                    if transcript_response.ok:
                        summary_chapter_response['transcript'] = transcript_response.json(
                        )

                if 'chaptering_url' in result['file']:
                    chaptering_url = result['file']['chaptering_url']
                    chaptering_response = requests.get(chaptering_url)
                    if chaptering_response.ok:
                        summary_chapter_response['chapters'] = chaptering_response.json(
                        )

                if 'final_summary' in result['file']:
                    summary_chapter_response['summary'] = result['file']['final_summary']

                summary_chapter_response['fileId'] = response['file']['id']
                return summary_chapter_response
            else:
                return {'error': 'Unknown error, summarization and chapter extraction failed'}
        return response
