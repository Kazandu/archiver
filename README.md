# archiver
A tool to automate the workflow of archiving youtube videos.

--ignore-archive Ignores the archivelist.txt (For redownloading Videos)

### Features

Watchdog
- (WIP) Monitor channels and automatically live record via [ytarchive](https://github.com/Kethsar/ytarchive)
- (WIP) Scrape twitter and the youtube community tab for Member-only videos and automatically live record via [ytarchive](https://github.com/Kethsar/ytarchive)
- (WIP) Pass video links to the checker to download the converted version
- Probably more, if you have ideas open an issue

Checker
- Checks youtube links in checker_batch.txt for conversion status (https | vp9)
- Moves converted video links to the downloader batch

Downloader
- Downloads youtube videos one by one from dl_batch.txt
- Converts youtube .srv3 subtitles with close to original formatting to .ass with [YTSubConverter](https://github.com/arcusmaximus/YTSubConverter)
- Optional execution of post download scripts (Example with rclone included, useful for VPS's with not enough storage)



Thanks to the yt-dl/yt-dlp Team, kethsar for ytarchive and arcusmaximus for YTSubConverter, you guys make archiving Youtube videos really easy!
