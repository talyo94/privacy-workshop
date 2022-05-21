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

function createBotLabel() {
  const lbl = document.createElement("div");
  // lbl.append(document.createTextNode("BOT"));
  const img = document.createElement("img");
  img.src =
    "https://thumbs.dreamstime.com/b/ai-robot-head-chat-bot-icon-isolated-white-background-ai-robot-head-chat-bot-icon-109860127.jpg";
  img.height = 40;
  img.width = 40;
  lbl.append(img);
  return lbl;
}
function findUsers() {
  //"//article//header/div[2]/div[1]/div/div/span" - all the way to the span of name
  let nodesSnapshot = getElementByXpath("//article//header/div[2]");

  for (var i = 0; i < nodesSnapshot.snapshotLength; i++) {
    console.log("ITEM:", i, nodesSnapshot.snapshotItem(i));
    nodesSnapshot.snapshotItem(i).appendChild(createBotLabel());
  }
}

findUsers();
