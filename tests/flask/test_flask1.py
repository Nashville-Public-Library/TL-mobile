from app.pwa.pod import Podcast

def test_delete_me():
    '''just something to get the structure up and running'''
    show: str = "scene"
    mah = Podcast(show=show)
    assert type(mah.to_client()) == dict