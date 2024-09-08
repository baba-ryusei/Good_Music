from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupForm,Song
from .models import Group
from .forms import SongForm

# Create your views here.
def frontpage(request):
    return render(request,"page/frontpage.html")


def create_play(request):
    if request.method == 'POST':
        song_form = SongForm(request.POST)
        if song_form.is_valid():
            group_name = song_form.cleaned_data['group_name']
            # グループを検索、なければ新規作成
            group, created = Group.objects.get_or_create(name=group_name)
            
            # 曲を保存してグループに関連付ける
            song = song_form.save(commit=False)
            song.group = group
            song.save()

            return redirect('play_list')  # プレイリスト一覧にリダイレクト
    else:
        song_form = SongForm()

    return render(request, 'page/create_play.html', {
        'song_form': song_form
    })

def group_list(request):
    groups = Group.objects.all()
    songs = []  # 初期化
     # もし「いいね数でソート」のリクエストがあれば、それに従ってソートする
    if request.GET.get('sort_by_likes'):
        # いいね数でソートされた曲リストを取得
        songs = list(Song.objects.all())  # クエリセットをリストに変換
        songs_sorted_by_likes = sorted(songs, key=lambda song: song.likes, reverse=True)
    else:
        songs_sorted_by_likes = Song.objects.all()  # クエリセット

    context = {
        'groups': groups,
        'songs_sorted_by_likes': songs_sorted_by_likes,
    }

    return render(request, 'page/play_list.html', context)
# グループ詳細ページ
def group_detail(request, group_id):
    group = get_object_or_404(Group, group_id=group_id)
    songs = group.songs.all()  # グループに関連する曲を取得

    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.group = group  # グループに曲を紐付ける
            song.save()
            return redirect('play_detail', group_id=group_id)
    else:
        form = SongForm()

    return render(request, 'page/play_detail.html', {'group': group, 'songs': songs, 'form': form})

# 曲の削除機能
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    group_id = song.group.group_id  # 曲が属しているグループのIDを取得
    song.delete()
    return redirect('play_detail', group_id=group_id)

# アーティスト名を削除するビュー
def delete_artist(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    song.artist = ''  # アーティスト名を空にする
    song.save()
    return redirect('play_list')

# グループ削除のビュー
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('play_list')  # 削除後、プレイリスト一覧にリダイレクト

# いいねを追加または削除するためのビュー
def like_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    # リクエストユーザーがすでにいいねを押しているか確認するロジック（ユーザーごとにいいねを管理する場合）
    # 今回は単純にいいね数を増減させる例を示します
    if 'liked' in request.session:
        # 既にいいねを押している場合
        if request.session['liked'] == song_id:
            song.likes -= 1
            request.session['liked'] = None  # いいねを解除
        else:
            song.likes += 1
            request.session['liked'] = song_id  # 新しくいいね
    else:
        song.likes += 1
        request.session['liked'] = song_id
    
    song.save()
    return redirect('play_list')  # プレイリスト一覧ページにリダイレクト

def playlist_view(request):
    # グループと曲のデフォルトの取得
    groups = Group.objects.all()

    # いいね数でソートされた曲のリストを取得
    if request.GET.get('sort_by_likes'):
        songs_sorted_by_likes = Song.objects.order_by('-likes')
    else:
        songs_sorted_by_likes = []

    context = {
        'groups': groups,
        'songs_sorted_by_likes': songs_sorted_by_likes,
    }
    return render(request, 'page/playlist.html', context)
