from pyyoutube import Api
import re

# '' ""

def prepare_str(text):
    return text.replace('&quot;', '\"').replace("&#39;", "\'").replace("&amp;", "&")

# '' ""
def video_title(url):
    if re.search("list=", url):
        return "Playlist "

    api = Api(api_key="AIzaSyDcdVmOCOABKydxtgqP7H8ucvRSpIxDnP4")

    if re.search(r"(&|\?)t=\d+[s]?", url):
        url = re.sub(r"(&|\?)t=\d+[s]?", "", url)


    if re.search("&ab_channel=", url):
        url = url.split("&ab_channel=")
        url = url[0]

    url = re.sub(r"http[s]?://", "", url)
    url = re.sub(r"www\.youtube\.com/(watch\?v=|embed/)", "", url)
    video_id = url.replace("youtu\.be\/", "")


    data = api.get_video_by_id(video_id=video_id, return_json=True)
    data = data["items"][0]["snippet"]["title"]
    return prepare_str(data)


# '' "" AIzaSyDcdVmOCOABKydxtgqP7H8ucvRSpIxDnP4
def yt_search(search, searches):
    s_links = []
    s_titles = []
    s_thumbnail_url = []

    api = Api(api_key="AIzaSyDcdVmOCOABKydxtgqP7H8ucvRSpIxDnP4")
    data = api.search_by_keywords(
        q=search, search_type=["video", "playlist"], count=searches).to_dict()

    data = data["items"]
    # print(data[0])
    for video_data in data:
        key = "videoId" if video_data["id"]["kind"] == "youtube#video" else "playlistId"
        before_id = "/playlist?list=" if key == "playlistId" else "/watch?v="
        title = prepare_str(video_data["snippet"]["title"])
        if title in s_titles:
            old_name = title
            n = 1
            while True:
                if title in s_titles:
                    title = f"{old_name}{n*' '}"
                else:
                    break

                n += 1

            s_titles.append(title)

        else:
            s_titles.append(title)

        s_thumbnail_url.append(prepare_str(video_data["snippet"]["thumbnails"]["default"]["url"]))
        s_links.append(f'{before_id}{video_data["id"][key]}')


    return s_titles, s_links, s_thumbnail_url

# ''


if __name__ == "__main__":
    while True:
        search = input("search id: ")
        print(video_title(search))

