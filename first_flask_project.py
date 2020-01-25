from flask import Flask, render_template, request, url_for, redirect  # сперва подключим модуль

from stepik_media_data import videos, playlists, tags

app = Flask(__name__)  # объявим экземпляр фласка


STEPIK_MEDIA_TITLE = "Stepik Media"

def get_search_video(search_word, playlists=playlists, tags=tags, videos=videos):
    result_searching = {}

    def search_video(search_word, search_place, video_places, result_searching,
                     video_data=videos):
        if search_word in search_place:
            for video in video_places:
                video_id = video
                video_title = video_data[video]['title']
                video_link = video_data[video]['video_link']
                result_searching[video_id] = [video_title, video_link]

    search_word = search_word.strip().lower()
    for playlist in playlists:
        playlist_title = playlists[playlist]['title']
        playlist_videos = playlists[playlist]['videos']
        search_video(search_word, playlist_title.lower(), playlist_videos, result_searching)

    for tag in tags:
        tag_videos = tags[tag]['videos']
        search_video(search_word, tag.lower(), tag_videos, result_searching)

    for video in videos:
        title_search_video = videos[video]['title']
        if search_word in title_search_video:
            video_id = video
            video_title = videos[video]['title']
            video_link = videos[video]['video_link']
            if video_id not in result_searching:
                result_searching[video_id] = [video_title, video_link]
        else: continue
    if result_searching == {} or search_word == "": result_searching = None
    return result_searching


@app.route('/', methods=['POST', 'GET'])
def main():
    index_page_title = 'Портал видео, посвященных программированию'
    index_page_text = 'Материалы для тех, кто учится программировать'
    playlist_video_link = {}
    if request.method == 'POST':
        search_word = request.form.get('index_search_bar').strip()
        if search_word == None or search_word == "": pass
        else:
            return redirect('/search/{}'.format(search_word))
    for playlist in playlists:
        video_id = playlists[playlist]['videos'][0]
        playlist_video_link[playlist] = videos[video_id]['video_link']


    return render_template('index.html', page_title=index_page_title, page_text=index_page_text, tags=tags,
                           playlists=playlists, playlist_video_link=playlist_video_link)


@app.route('/about')
def about():
    about_page_title = '{} – О приложении'.format(STEPIK_MEDIA_TITLE)
    about_text = '{} – Это кинотеатр полезных видео, посвященных программированию'.format(STEPIK_MEDIA_TITLE)
    about_output = render_template("about.html",  page_title=about_page_title, page_text=about_text)
    return about_output


@app.route('/playlists/<pl_id>/<v_id>/', methods=['POST', 'GET'])
@app.route('/playlists/<pl_id>/', methods=['POST', 'GET'])
def playlist(pl_id, v_id='1'):
    try:
        playlist_id = int(pl_id) - 1
        video_id = int(v_id)
        video_number = 1
        max_v_id_in_playlist = len(playlists[playlist_id]['videos'])
        playlist = {'title': playlists[playlist_id]['title'], 'videos': [],
                    'description': playlists[playlist_id]['description']}
        video_on_page = {}
        for video in playlists[playlist_id]['videos']:
            video_title = '{}. {}'.format(str(video_number), videos[video]['title'])
            video_link = videos[video]['video_link']
            video_route = '/playlists/{}/{}'.format(pl_id, video_number)
            playlist['videos'].append([video_title, video_link, video_route])
            if video_number == video_id:
                video_on_page = videos[video]
            video_number += 1
        if request.method == 'POST':
            if int(v_id) < max_v_id_in_playlist:
                next_video = int(v_id)+1
            else: next_video = v_id
            return redirect('/playlists/{}/{}'.format(pl_id, str(next_video)))
        playlist_output = render_template("playlist.html", playlist=playlist, video_on_page=video_on_page)
        return playlist_output
    except ValueError:
        return page_not_found(404)


@app.route('/search/<search_word>', methods=['POST', 'GET'])
@app.route('/search/', methods=['POST', 'GET'])
def search(search_word=None):
    search_result = None
    search_message = "Введите слова для поиска"
    if request.method == 'POST':
        search_word = request.form.get('search_bar').strip()
    if search_word == None or search_word == "": pass
    else:
        search_result = get_search_video(search_word)
        if search_result == None: search_message = 'По Вашему запросу ничего не найдено'
        else:
            for playlist in playlists:
                for video in search_result:
                    if video in playlists[playlist]['videos']:
                        video_id = playlists[playlist]['videos'].index(video) + 1
                        playlist_id = playlist + 1
                        video_route = '/playlists/{}/{}'.format(playlist_id, video_id)
                        search_result[video].append(video_route)
            search_message = 'Результат поиска по запросу "{}": {} видео'.format(search_word, len(search_result))

    search_output = render_template("searchpage.html", tags=tags, search_result=search_result,
                                    search_message=search_message)
    return search_output


@app.errorhandler(404)
def page_not_found(error):
    return "Такой страницы нет"


app.run()
