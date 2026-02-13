from playwright.sync_api import Page

def test_first_load_1(desktop: Page):
    assert "NTL" in desktop.title()

def test_first_load_2(desktop: Page):
    '''will show the "install on mobile" screen when accessed on desktop'''
    desktop.wait_for_selector(".mobileOnlySpeech")
    assert desktop.locator(".mobileOnlySpeech").count() > 0

def test_mobile_not_installed_1(mobile_not_installed: Page):
    mobile_not_installed.wait_for_selector(".installDialog")
    assert mobile_not_installed.locator(".installDialog").count() > 0

def test_mobile_not_installed_2(mobile_not_installed: Page):
    mobile_not_installed.wait_for_selector(".installDialog")
    assert mobile_not_installed.get_by_text("To install the app:").is_visible()
    assert mobile_not_installed.get_by_text("On Apple Phones:").is_visible()
    assert mobile_not_installed.get_by_text("On Android Phones:").is_visible()

def test_mobile_installed_1(mobile_installed: Page):
    '''checking if home screen logo is on page'''
    mobile_installed.wait_for_selector(".logo-container")
    assert mobile_installed.locator(".logo-container").count() > 0

def test_schedule_1(mobile_installed: Page):
    '''navigate to /schedule page and check if various content is loaded'''
    mobile_installed.wait_for_selector('a[href="#/schedule"]').click()
    mobile_installed.wait_for_selector(".dailyScheduleLinksContainer")
    assert mobile_installed.get_by_text("Schedules").is_visible()
    assert mobile_installed.get_by_text("Tuesday").is_visible()
    assert mobile_installed.get_by_text("Broadcast Schedule").is_visible()

def test_schedule_daily_1(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/schedule"]').click()
    mobile_installed.wait_for_selector('a[href="#/schedule/monday"]').click()
    mobile_installed.wait_for_selector(".dailyScheduleHeader")
    mobile_installed.wait_for_selector(".dailyScheduleContainerIndividual")
    assert "Monday" in mobile_installed.locator(".dailyScheduleHeader").text_content()
    assert mobile_installed.locator(".dailyScheduleContainerIndividual").count() > 0

def test_podcasts_1(mobile_installed: Page):
    '''navigate to /podcasts page and check if various content is loaded'''
    mobile_installed.wait_for_selector('a[href="#/podcasts"]').click()
    mobile_installed.wait_for_selector(".podcastIndividual")
    mobile_installed.wait_for_selector("#categorySelector")
    assert mobile_installed.locator(".podcastIndividual").count() > 0
    assert mobile_installed.locator("#categorySelector").count() > 0

def test_podcast_individual_1(mobile_installed: Page):
    '''navigate to /podcasts page, load individual podcast, check if various content is loaded. Checklist chosen at random'''
    mobile_installed.wait_for_selector('a[href="#/podcasts"]').click()
    mobile_installed.wait_for_selector("#checklist")
    mobile_installed.locator("#checklist").click()
    mobile_installed.wait_for_selector("#podcastIndividualTitle")
    assert "Checklist" in mobile_installed.locator("#podcastIndividualTitle").inner_text()

def test_podcast_individual_2(mobile_installed: Page):
    '''navigate to /podcasts page, load individual podcast, check if various content is loaded. Checklist chosen at random.'''
    mobile_installed.wait_for_selector('a[href="#/podcasts"]').click()
    mobile_installed.wait_for_selector("#checklist")
    mobile_installed.locator("#checklist").click()
    mobile_installed.wait_for_selector(".podcastEpisodeTitle")
    assert mobile_installed.locator(".podcastEpisodeTitle").count() > 0

def test_about_1(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/about"]').click()
    mobile_installed.wait_for_selector(".aboutIconsContainer")
    assert mobile_installed.locator(".aboutIconsContainer").count() > 0
 
def test_about_2(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/about"]').click()
    mobile_installed.wait_for_selector(".aboutIcons")
    assert mobile_installed.locator(".aboutIcons").count() > 0

def test_privacy_1(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/about"]').click()
    mobile_installed.wait_for_selector('a[href="#/privacy"]').click()
    mobile_installed.wait_for_selector("h1")
    assert "Privacy" in mobile_installed.locator("h1").text_content()

def test_feedback_1(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/about"]').click()
    mobile_installed.wait_for_selector('a[href="#/feedback"]').click()
    mobile_installed.wait_for_selector("h1")
    assert "Feedback" in mobile_installed.locator("h1").text_content()

def test_settings_1(mobile_installed: Page):
    mobile_installed.wait_for_selector('a[href="#/about"]').click()
    mobile_installed.wait_for_selector('a[href="#/settings"]').click()
    mobile_installed.wait_for_selector("h1")
    assert "Settings" in mobile_installed.locator("h1").text_content()