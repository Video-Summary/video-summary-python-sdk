from setuptools import setup, find_packages

setup(
    name='video-summary',
    version='1.0.0',
    author='Video Summary',
    author_email='hi@videosummary.io',
    description='A Python SDK for video processing, providing functionalities like speech-to-text, summarization, transcription, and chaptering.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Video-Summary/video-summary-python-sdk',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        # Add other dependencies as required
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='video processing, speech-to-text, video summarization, transcription, chaptering',
    project_urls={
        'Documentation': 'https://github.com/Video-Summary/video-summary-python-sdk#readme',
        'Source': 'https://github.com/Video-Summary/video-summary-python-sdk',
        'Tracker': 'https://github.com/Video-Summary/video-summary-python-sdk/issues',
    },
)
