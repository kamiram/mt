chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'inboxsdk__injectPageWorld' && sender.tab) {
    if (chrome.scripting) {
      // MV3
      chrome.scripting.executeScript({
        target: { tabId: sender.tab.id },
        world: 'MAIN',
        files: ['pageWorld.js'],
      });
      sendResponse(true);
    } else {
      // MV2 fallback. Tell content script it needs to figure things out.
      sendResponse(false);
    }
  }
});

chrome.runtime.onInstalled.addListener(function (object) {
    let externalUrl = "https://mailtracker.mckira.com/";

        console.log("Try to launch");
        chrome.tabs.create({ url: externalUrl }, function (tab) {
            console.log("We are installed");
        });
});