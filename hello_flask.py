from flask import Flask, render_template, request    # сперва подключим модуль

from stepik_media_data import videos, playlists, tags

app = Flask(__name__)      # объявим экземпляр фласка

STEPIK_MEDIA_TITLE = 'Stepik Media'


@app.route('/')
def main():
    index_title = STEPIK_MEDIA_TITLE
    index_page_title = 'Портал видео, посвященных программированию'
    start_msg_to_user = 'Теги: '
    for tag in tags.keys():
        start_msg_to_user += tag + ', '
    start_msg_to_user = start_msg_to_user[0:-2] # убираем запятую после последнего тега /
    start_msg_to_user += '<br>Плейлисты: '
    for playlist in playlists:
        start_msg_to_user += playlists[playlist]["title"] + " ({} видео)".format(len(playlists[playlist]["videos"])) + ', '
    start_msg_to_user = start_msg_to_user[0:-2] # убираем запятую после последнего плейлиста /
    #return start_msg_to_user
    return render_template('index.html', index_title = index_title, index_page_title = index_page_title, tags=tags)

@app.route('/about')
def about():
    about_title = STEPIK_MEDIA_TITLE
    about_page_title = '{} – О приложении.'.format(about_title)
    about_text = '{} – Это кинотеатр полезных видео, посвященных программированию'.format(about_title)
    about_output = render_template("about.html", about_title = about_title, about_page_title = about_page_title,
                             about_text = about_text)
    return about_output

'''@app.route('/videos/<id>')
def video(id):
    video_id = int(id) - 1
    if video_id in videos:
        video_msg = 'Название: ' + videos[video_id]['title'] + '<br>'
    else:
        video_msg = 'Такого видео у нас нет, всего хорошего!<br>'
    video_msg += 'Теги: '
    for tag in tags.keys():
        if video_id in tags[tag]["videos"]:
            video_msg += tag + ', '
    video_msg = video_msg[0:-2]
    video_msg += '<br>Видео: ' + videos[video_id]["video_link"]
    return video_msg'''


@app.route('/playlists/<pl_id>/<v_id>/')
@app.route('/playlists/<pl_id>/')
def playlist(pl_id, v_id=1):
    try:
        playlist_id = int(pl_id) - 1
        video_id = int(v_id)
        video_number = 1
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
        playlist_output = render_template("playlist.html", playlist=playlist, video_on_page = video_on_page)
        return playlist_output
    except ValueError:
        return page_not_found(404)

@app.route('/search/', methods=['POST', 'get'])
def search():
    search_title = STEPIK_MEDIA_TITLE
    search_counter = 0
    search_result = {}

    if request.method == 'POST':
        search_name = request.form.get('search_bar').strip()
        for video in videos:
            #print(search_name, videos[video]['title'])
            if search_name.lower() in videos[video]['title'].lower():
                search_counter += 1
                search_result[search_counter] = videos[video]['video_link']
    print(search_result)
    search_output = render_template("searchpage.html", search_title = search_title, tags=tags)
    return search_output



@app.route('/tags/<tag>')
def thetag(tag):
    tag_msg = 'У нас есть {} видео по тегу: {}<br><br>'.format(len(tags[tag]['videos']), tag)
    tag_cnt = 1
    for video in tags[tag]['videos']:
        tag_msg += '{} . '.format(tag_cnt) + videos[video]['title'] + '<br>' + videos[video]['video_link'] + '<br><br>'
        tag_cnt += 1
    tag_msg += '<br>Приятного просмотра!'
    return tag_msg

@app.errorhandler(404)
def page_not_found(error):
   return "Такой страницы нет"

app.run()

