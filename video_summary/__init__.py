from .sdk import VideoSummarySDK

# Define a constant for the base URL, replacing it with your actual URL
BASE_URL = 'https://api.videosummary.io'


def get_sdk(api_key, base_url=BASE_URL):
    return VideoSummarySDK(api_key, base_url)
