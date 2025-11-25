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
    mobile_installed.wait_for_selector(".logo-container")
    assert mobile_installed.locator(".logo-container").count() > 0

def test_schedule_1(mobile_installed: Page, server):
    '''navigate to /schedule page and check if various content is loaded'''
    mobile_installed.evaluate("window.location.hash = '#/schedule'")
    mobile_installed.wait_for_selector(".dailyScheduleLinksContainer")
    assert mobile_installed.get_by_text("Schedules").is_visible()
    assert mobile_installed.get_by_text("Tuesday").is_visible()
    assert mobile_installed.get_by_text("Broadcast Schedule").is_visible()

def test_podcasts_1(mobile_installed: Page, server):
    '''navigate to /podcasts page and check if various content is loaded'''
    mobile_installed.evaluate("window.location.hash = '#/podcasts'")
    mobile_installed.wait_for_selector(".podcastIndividual", state="visible")
    mobile_installed.wait_for_selector("#categorySelector", state="visible")
    assert mobile_installed.locator(".podcastIndividual").count() > 0
    assert mobile_installed.locator("#categorySelector").count() > 0

def test_podcast_individual_1(mobile_installed: Page, server):
    '''navigate to /podcasts page, load individual podcast, check if various content is loaded. Checklist chosen at random'''
    mobile_installed.evaluate("window.location.hash = '#/podcasts'")
    mobile_installed.wait_for_selector("#checklist", state="visible")
    mobile_installed.locator("#checklist").click()
    mobile_installed.wait_for_selector("#podcastIndividualTitle", state="visible")
    assert "Checklist" in mobile_installed.locator("#podcastIndividualTitle").inner_text()

def test_podcast_individual_2(mobile_installed: Page, server):
    '''navigate to /podcasts page, load individual podcast, check if various content is loaded. Checklist chosen at random.'''
    mobile_installed.evaluate("window.location.hash = '#/podcasts'")
    mobile_installed.wait_for_selector("#checklist", state="visible")
    mobile_installed.locator("#checklist").click()
    mobile_installed.wait_for_selector(".podcastEpisodeTitle", state="visible")
    assert mobile_installed.locator(".podcastEpisodeTitle").count() > 0