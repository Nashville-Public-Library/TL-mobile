from playwright.sync_api import Page

def test_first_load_1(page: Page, server):
    page.goto(server)
    assert "NTL" in page.title()

def test_first_load_2(page: Page, server):
    '''will show the "install on mobile" screen when accessed on desktop'''
    page.goto(server)
    assert page.locator(".mobileOnlySpeech").count() > 0