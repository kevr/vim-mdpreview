
function join(delim, args) {
  if (args.length === 0)
    return null;

  let str = args[0];
  console.log(str);
  args = args.slice(1);
  for (const i in args) {
    const arg = args[i];
    str += delim + arg;
  }
  return str;
}

function make_websocket() {
  const base = location.hostname + ":" + location.port;
  console.log(base);
  const uri = join('', ["ws://", base, "/websocket"]);
  console.log(uri);
  const socket = new WebSocket(uri);

  socket.addEventListener("open", function() {
    console.log("Connected to websocket at " + uri);
  });

  socket.addEventListener("message", function(event) {
    const data = JSON.parse(event.data);
    console.log("Received websocket message: " + event.data);
    if (data.message === "reload") {
      console.log("Reloading!");
      location.reload();
    }
  });

  socket.addEventListener("close", function() {
    console.log("Disconnected, reconnecting soon...");
    setTimeout(make_websocket, 2500);
  });
}

make_websocket();
