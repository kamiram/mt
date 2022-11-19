/******/ (() => { // webpackBootstrap
var __webpack_exports__ = {};
/*!***************************************************!*\
  !*** ./node_modules/@inboxsdk/core/background.js ***!
  \***************************************************/
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

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYmFja2dyb3VuZC5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxrQkFBa0Isc0JBQXNCO0FBQ3hDO0FBQ0E7QUFDQSxPQUFPO0FBQ1A7QUFDQSxNQUFNO0FBQ047QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vaGVsbG8td29ybGQvLi9ub2RlX21vZHVsZXMvQGluYm94c2RrL2NvcmUvYmFja2dyb3VuZC5qcyJdLCJzb3VyY2VzQ29udGVudCI6WyJjaHJvbWUucnVudGltZS5vbk1lc3NhZ2UuYWRkTGlzdGVuZXIoKG1lc3NhZ2UsIHNlbmRlciwgc2VuZFJlc3BvbnNlKSA9PiB7XG4gIGlmIChtZXNzYWdlLnR5cGUgPT09ICdpbmJveHNka19faW5qZWN0UGFnZVdvcmxkJyAmJiBzZW5kZXIudGFiKSB7XG4gICAgaWYgKGNocm9tZS5zY3JpcHRpbmcpIHtcbiAgICAgIC8vIE1WM1xuICAgICAgY2hyb21lLnNjcmlwdGluZy5leGVjdXRlU2NyaXB0KHtcbiAgICAgICAgdGFyZ2V0OiB7IHRhYklkOiBzZW5kZXIudGFiLmlkIH0sXG4gICAgICAgIHdvcmxkOiAnTUFJTicsXG4gICAgICAgIGZpbGVzOiBbJ3BhZ2VXb3JsZC5qcyddLFxuICAgICAgfSk7XG4gICAgICBzZW5kUmVzcG9uc2UodHJ1ZSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIE1WMiBmYWxsYmFjay4gVGVsbCBjb250ZW50IHNjcmlwdCBpdCBuZWVkcyB0byBmaWd1cmUgdGhpbmdzIG91dC5cbiAgICAgIHNlbmRSZXNwb25zZShmYWxzZSk7XG4gICAgfVxuICB9XG59KTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==