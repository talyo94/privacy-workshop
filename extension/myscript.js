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
  // const r = /^\/\w+\/$/;
  const r = /^\/[a-zA-Z0-9\._]+\/$/;

  const userNodes = {};

  document.querySelectorAll('a[href^="/"').forEach((node) => {
    const href = node.getAttribute("href");
    if (href.startsWith("/explore")) {
      return;
    }
    const isUser = r.test(href);
    if (isUser) {
      const username = href.replaceAll("/", ""); // get the username
      if (!userNodes[username]) {
        userNodes[username] = [];
      }
      userNodes[username].push(node); // add node to reference
    }
  });
  if (Object.keys(userNodes).length > 0)
    fetch("http://localhost:8000/score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({ users: Object.keys(userNodes) }), // send usernames
    })
      .then((response) => response.json())
      .then((data) => {
        document.querySelectorAll(`.${BOT_LABEL_CLS}`).forEach((node) => {
          node.remove();
        });
        Object.keys(data).forEach((username) => {
          const fakeScore = data[username].score_is_fake;
          if (userNodes[username]) {
            userNodes[username].forEach((node) => {
              const lbl = createBotLabel(fakeScore);
              node.append(lbl); // put bot labels next to nodes
            });
          }
        });
      });
}

findUsers();

setInterval(() => {
  findUsers();
}, 5000);
