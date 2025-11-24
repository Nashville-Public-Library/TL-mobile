from playwright.sync_api import Page

def test_first_load_1(desktop: Page, server):
    desktop.goto(server)
    assert "NTL" in desktop.title()

def test_first_load_2(desktop: Page, server):
    '''will show the "install on mobile" screen when accessed on desktop'''
    desktop.goto(server)
    assert desktop.locator(".mobileOnlySpeech").count() > 0

def test_mobile_installed_1(mobile_installed: Page, server):
    '''checking if home screen logo is on page'''
    mobile_installed.goto(server)
    mobile_installed.wait_for_selector(".logo-container")
    assert mobile_installed.locator(".logo-container").count() > 0

def test_schedule_1(mobile_installed: Page, server):
    mobile_installed.goto(server)
    mobile_installed.evaluate("window.location.hash = '#/schedule'")
    mobile_installed.wait_for_selector(".dailyScheduleLinksContainer")
    assert mobile_installed.get_by_text("Schedules").is_visible()
    assert mobile_installed.get_by_text("Tuesday").is_visible()
    assert mobile_installed.get_by_text("Broadcast Schedule").is_visible()

def test_podcast_1(mobile_installed: Page, server):
    mobile_installed.goto(server)
    mobile_installed.evaluate("window.location.hash = '#/podcasts'")
    mobile_installed.wait_for_selector(".podcastIndividual")
    mobile_installed.wait_for_selector("#categorySelector")
    assert mobile_installed.locator(".podcastIndividual").count() > 0
    assert mobile_installed.locator("#categorySelector").count() > 0