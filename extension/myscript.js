// "content_scripts": [
//   {
//     "matches": ["*://*.instagram.com/*"],
//     "run_at": "document_end",
//     "js": ["myscript.js"]
//   }
// ]
function getElementByXpath(path) {
  return document.evaluate(
    path,
    document,
    null,
    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
    null
  );
}

function createBotLabel(fakePercentage) {
  const lbl = document.createElement("span");
  lbl.className = "bot-label";
  const img = document.createElement("img");
  img.src = chrome.runtime.getURL("user.svg");
  img.height = 12;
  img.width = 12;
  if (fakePercentage > 0.7) {
    img.style.filter =
      "invert(48%) sepia(79%) saturate(100) hue-rotate(0deg) brightness(118%) contrast(119%)";
  } else if (fakePercentage < 0.3) {
    img.style.filter =
      "invert(48%) sepia(79%) saturate(100) hue-rotate(89deg) brightness(118%) contrast(119%)";
  } else {
    img.style.filter =
      "invert(48%) sepia(79%) saturate(100) hue-rotate(89deg) brightness(118%) contrast(119%)";
  }
  lbl.append(img);
  return lbl;
}

function findUsers() {
  const BOT_LABEL_CLS = "bot-label";
  const r = /^\/\w+\/$/;

  document.querySelectorAll(`.${BOT_LABEL_CLS}`).forEach((node) => {
    node.remove();
  });

  document
    .querySelectorAll('a[href^="/"')

    .forEach((node) => {
      const href = node.getAttribute("href");
      if (href.startsWith("/explore")) {
        return;
      }
      const isUser = r.test(href);
      if (isUser) {
        // node.style["color"] = "#f8f8f8";
        const lbl = createBotLabel(Math.random());
        node.append(lbl);
      }
    });
}

findUsers();
