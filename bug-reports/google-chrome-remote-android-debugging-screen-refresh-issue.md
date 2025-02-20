# Google Chrome remote Android debugging screen refresh issue

## Report sent 2025-02-19

### Text in free text area (with Chrome version information redacted) in response to "Describe the issue in detail"

When I do remote Android debugging connecting my phone to my laptop via USB, I encounter an issue where the phone screen copy shown on the laptop sometimes stops updating, even though the devtools connection is still running fine, as evidenced in these ways: actions on the laptop are reflected on the actual phone screen, and new information keeps coming into the network panel in the devtools on the laptop.

During this period where the phone screen copy on the laptop fails to update, the url bar shown on the laptop does continue to update for full page navigations, but not for single-page app navigations.

In some cases, switching the active panel of devtools (from console panel to network panel or vice versa) forces the phone screen copy on the laptop to update ad match the actual phone screen. In the immediate aftermath of this, updating seems to work normally. However, sometimes, switching the active panel of devtools has no effect.

I was able to replicate this on https://web.dev/ which is a basic and standards-compliant website designed as a single-page app. When I navigate to the website, it loads in dark mode on my phone due to my dark mode preference on the phone (after briefly initially loading in light mode and then switching). However, the phone screen copy on the laptop shows the webpage in light mode, failing to update it to dark mode when the phone screen does. Scrolling actions (initiated on either the phone or the laptop) cause the screen to scroll on the phone but not on the laptop. Clicking on any of the page's "Learn more links navigates the phone to a new page (this is a single-page app navigation) but again does not update the phone screen copy seen on the laptop. And since it's a single-page app navigation, it also fails to update the url bar on the laptop (while updating it on the phone screen). When I switch from the console panel to the network panel, the phone screen copy on the laptop updates, though the url bar is still outdated.

I was also able to replicate this by visiting https://stackoverflow.com/ which is not a single-page app. I clicked "Accept all cookies" through my laptop, which caused cookies to be accepted on the phone screen, but the phone screen copy on the laptop failed to refresh. The phone screen copy on the laptop also failed to update when I scrolled on the phone. When I clicked on the phone screen to https://stackoverflow.com/questions/79453334/power-apps-is-there-a-way-to-declare-a-syntax-as-variable-and-reuse-across-my (one of the links on the page at the time of my visit) the phone screen went to the new url. The phone screen copy on the laptop did not refresh, though the url bar on the laptop did refresh. Switching the active panel in devtools from the network panel to the console panel led the phone screen copy on the laptop to update.

Both my laptop and my Android phone device are running Chrome 133.

Device information:

Chrome version on laptop: private

Chrome version on Android device: private

I also tried this with another Android device and replicated the same issues.

### Additional options

URL: https://web.dev/

Email: vipulnaik1@gmail.com

Attach file: (none, as Chrome auto-suggested a screenshot of the right inspect tab)

Boxes checked:

* We may email you for more information and updates
* Include this screenshot and titles of open tabs
* Send system information (I clicked the link and confirmed that this
  includes he Chrome version on the laptop and a few select Chrome
  settings)
