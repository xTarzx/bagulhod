from youtubesearchpython.__future__ import VideosSearch


async def search_youtube(term):
    res = []
    videos = VideosSearch(term, limit=10)
    result = await videos.next()

    result = result.get("result")

    for entry in result:
        title = entry.get("title")
        url = entry.get("link")
        thumbnail = entry.get("thumbnails")[0].get("url")
        res.append({"title": title, "url": url, "thumbnail": thumbnail})

    return res
