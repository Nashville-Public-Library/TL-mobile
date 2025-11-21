from app.pwa.pod import Podcast

def test_Podcast_Object_1():
    show: str = "scene"
    mah = Podcast(show=show)
    assert type(mah.to_client()) == dict

def test_Podcast_Object_2():
    show: str = "scene"
    mah = Podcast(show=show)
    client:dict = mah.to_client()
    episodes = client.get("episodes")
    assert type(episodes) == list
