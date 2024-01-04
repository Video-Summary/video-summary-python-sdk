# Video Summary SDK for Python

Enhance your video processing workflow with the `Video Summary SDK` for Python. This SDK offers a powerful and easy-to-use solution for transcribing, summarizing, and extracting chapter information from videos. It supports a wide range of sources, including local files and hosted URLs.

## Key Features

- **Transcription**: Accurately convert speech in videos into text.
- **Summarization**: Efficiently summarize video content.
- **Chapter Extraction**: Easily identify and extract distinct chapters from videos.
- **Versatile Source Support**: Compatible with local files, URLs, and various cloud storage solutions.

## Installation

Install the package using pip:

```bash
pip install video-summary
```
## Getting Started

First, obtain your free API key from [VideoSummary.io](https://videosummary.io?utm_source=github). Then, install the SDK and integrate it into your Python projects as follows:

```python
from video_summary import VideoSummarySDK

# Initialize the SDK with your API key
video_summary = VideoSummarySDK('your_api_key')

# Example usage
try:
    # Local file path or hosted video URL
    video_path = './path/to/your/video.mp4'
    result = video_summary.summarize(video_path)
    print("Video Summary Result:", result)
except Exception as e:
    print("Error using Video Summary SDK:", e)
```

## API Methods

The Python SDK offers several methods to interact with your videos. The `id` and `callback_url` parameters are optional. The `id` can be used for your reference if you have an asset ID. The `callback_url` is for receiving a webhook when the video processing is completed. 

If you don't provide a callback url, the call will be synchronous and wait for the processing to complete.

### `summarize(url, [id], [callback_url])`
Summarizes the video content. Provide the URL of the video, and optionally, include an ID and a callback URL for asynchronous processing.

### `transcribe(url, [id], [callback_url])`
Transcribes the audio content of the video into text. Input the video URL, and if desired, an ID and a callback URL.

### `chapter(url, [id], [callback_url])`
Extracts chapters from the video for easier navigation and understanding. This method requires the video URL, with optional ID and callback URL.

### `summarizeAndChapter(url, [id], [callback_url])`
Performs both summarization and chapter extraction on the video. Provide the video URL, and optionally, an ID and a callback URL.

Each method returns a response object containing relevant data about the video processing, including transcripts, summaries, chapters, and file IDs.





## output
```json 
{
  "transcript": {
    "speakers": [
      {
      "speaker": "SPEAKER_00",
      "text": " video",
      "timestamp": [10,10.26],
      "start": 10,
      "end": 10.26
    },
    {
      "speaker": "SPEAKER_00",
      "text": " products.",
      "timestamp": [10.26,10.9],
      "start": 10.26,
      "end": 10.9
    }
    ],
    "chunks": [
      { "text": " video", "timestamp": [Array] },
      { "text": " products", "timestamp": [Array] },
    ],
    "text": "..."
  },
  "chapters": [
    {
      "start": 0,
      "end": 10.9,
      "title": "Introduction to VideoSummary.io",
      "text": "Introducing videosummary.io. a simple api to transcribe, chapter and summarize audio and video files."
    }
  ],
  "summary": "Developers, check this out. You need VideoSummary.io in your life. It lets you build video products much easier with features like video summarization and video chaptering. Grab it now and start building game-changing video products.",
  "fileId": "xxx-xxx-4ffc-a2a5-13d3cee085dd"
}
```