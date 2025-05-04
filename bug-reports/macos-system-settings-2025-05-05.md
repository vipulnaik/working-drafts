# MacOS System Settings: 2025-05-05

I clicked to submit feedback via https://feedbackassistant.apple.com/
after logging in. The submission time was 2025-05-05 3:51 AM IST
(2025-05-04 22:21 UTC). The file upload too four minutes and the
feedback was submitted at 2025-05-05 3:55 AM IST (2025-05-04 22:25
UTC). The feedback is
[here](https://feedbackassistant.apple.com/feedback/17492146) (only
accessible to me when logged in).

## Fields before the free-form fields

Question: Please provide a descriptive title for your feedback:

WHAT I FILLED: Energy Saver preference update reverts due to interference between Lock Screen and Battery sections

Question: Which area are you seeing an issue with?

WHAT I SELECTED: System Settings

Notes: This is clearly the right option.

Question: What type of issue are you reporting?

WHAT I SELECTED: Incorrect/Unexpected Behavior

Notes: The other options were Application Crash, Application
Slow/Unresponsive, and Suggestion. The option I selected was clearly
the right one.

Which settings are you seeing issues with?

WHAT I SELECTED: Lock Screen

Notes: Ideally I should have selected both Lock Screen and Battery,
but the UI only allowed for one selection.

## What I entered in the free-form text area

I had two instances of System Settings changes I made on my `(device,
OS version (redacted for privacy))` that seemed to not take effect
when I next checked. Initially, I thought that I had hallucinated
making the change. But a closer digging into the Apple system logs
showed that I had made the changes, but a bug in MacOS caused them to
be reverted.

My inference as to the mechanism is that sometimes, changes to `Lock
Screen` and `Battery` (specifically, `Low Power Mode`) settings made
close by in time can result in the earlier setting change getting
reverted. I don't have a reliable way to reproduce, but both the
examples of this "in the wild" were of this sort, with both possible
orders (one where the `Lock Screen` change was made first and got
reverted by the `Low Power Mode` change, and one where the `Low Power
Mode` change was made first and got reverted by the `Lock Screen`
change).

For pulling logs, I did `sudo log show --last` in the terminal to
print logs over the relevant time range and then filtered to specific
minutes.

Due to the size limitation of 4096 characters on the text area, I
cannot include detailed log files showing the pattern (and I think the
sysdiagnose output likely doesn't show the issue because the last
occurrence was several hours ago). Here is one example of how the Low
Power Mode setting change led to the change to a "Lock Screen"
setting. To stay within 4096 characters, I have snipped out log lines
in between that are not directly relevant.

Successful update to Lock Screen setting ("Turn display off on power
adapter when inactive") from 10 minutes down to 1 minute:

```
2025-05-02 13:19:21.877663-0700  localhost authd[630]: [com.apple.Authorization:authd] Succeeded authorizing right 'system.preferences' by client '/System/Library/PrivateFrameworks/SystemAdministration.framework/XPCServices/writeconfig.xpc' [37316] for authorization created by '/System/Library/ExtensionKit/Extensions/LockScreen.appex' [37315] (2,0) (engine 2091)
[...]
2025-05-02 13:19:21.880036-0700  localhost powerd[530]: [com.apple.powerd:pmSettings] Energy Saver Prefs have changed
[...]
2025-05-02 13:19:21.881842-0700  localhost kernel[0]: PMRD: setAggressiveness(0) kPMMinutesToDim = 1
```

20 seconds later, this gets reverted back to 10 minutes as a result of
"Low Power Mode" being updated from "Only on Battery" to "Always":

```
2025-05-02 13:19:41.826786-0700  localhost authd[630]: [com.apple.Authorization:authd] Succeeded authorizing right 'system.preferences' by client '/System/Library/PrivateFrameworks/SystemAdministration.framework/XPCServices/writeconfig.xpc' [37316] for authorization created by '/System/Library/ExtensionKit/Extensions/PowerPreferences.appex' [77355] (2,0) (engine 2095)
2025-05-02 13:19:41.827677-0700  localhost powerd[530]: [com.apple.powerd:pmSettings] Energy Saver Prefs have changed
[...]
2025-05-02 13:19:41.829812-0700  localhost powerd[530]: [com.apple.powerd:pmSettings] Sleep timer 1 display timer 10
2025-05-02 13:19:41.829958-0700  localhost kernel[0]: PMRD: setAggressiveness(0) kPMMinutesToSleep = 0
2025-05-02 13:19:41.829976-0700  localhost kernel[0]: PMRD: setAggressiveness(0) kPMMinutesToDim = 10
```

I'm happy to provide additional logs or other details upon request!

## Files attached

* system profiler output file
* sysdiagnose output file

I tried uploading
`energy-saver-preferences-update-reverts-due-to-interference-between-lock-screen-and-battery-sections.md`
that has my more detailed diagnosis but the upload failed. It looks
like their interface only allows for files to be uploaded that look
like a system profiler output file or sysdiagnose output file.
