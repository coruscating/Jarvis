var ws;
var CONNECTING = 0;
var OPEN = 1;
var CLOSING = 2;
var CLOSED = 3;

function checkWebSocket() //check if the connection is open
{
    if (! ws){
        log(ERROR, 'No WebSocket');
        return false;
    }
    
    else if (ws.readyState != OPEN) {
        log(ERROR, 'WebSocket not ready');
        return false;
    }
    return true;
}



function WebSocketStart()
{
  if ("WebSocket" in window)
  {
     // Let us open a web socket
     ws = new WebSocket($('#WebSocketAddr').val());
     $('#experiment').html($('#WebSocketAddr  option:selected').text());
     log(NOTE, "Connected to server");
     
     
     $(".Websocket.ui-accordion-header").removeClass("off").addClass("on");
     
     ws.onopen = function()
     {
        ws.send("CONNLIST");
     };
     ws.onmessage = function (evt)
     {
         // message form: STATUS;1407784757.2;Shutters;Shutters461;CLOSE
        if(evt.data.length > 8){
            var string = evt.data.split(";");
            
            if(string[0]=="STATUS" || string[0]=="SPECIALREQUEST"){
                
                // check that function exists before trying to call it
                for(var key in window.deviceMap){
                  if (window.deviceMap[key]==string[2]){
                    log(NOTE, "Received: " + evt.data, string[2]);
                    window[string[2] + "ReceivedData"](evt.data);
                    dt = new Date();
                    var hours = dt.getHours();
                    var minutes = dt.getMinutes();
                    var seconds = dt.getSeconds();
                    // the above dt.get...() functions return a single digit
                    // so I prepend the zero here when needed
                    if (hours < 10)
                     hours = '0' + hours;
                    if (minutes < 10)
                     minutes = '0' + minutes;
                    if (seconds < 10)
                     seconds = '0' + seconds;
                    $('.' + string[2] + 'Update').html('Updated ' + hours + ":" + minutes + ":" + seconds);
                  }
                }
            } else if(string[0].substring(0,20) == "SPECIALREQUESTSCRIPT" || string[0].substring(0,10) == "PLOTSCRIPT"){
                ScriptReceivedData(evt.data);
            } else if(string[0] == "SPEAK"){
                log(SPEAK, string[1]);
            } else if(string[0] == "SCRIPTVAR"){
                window.Scripts[string[1]].ScriptVars[string[2]]=string[3].replace(/\r?\n|\r/g, "");
            } else if(string[0] == "SCRIPTOUTPUT"){
                ScriptOutput(string[1],string[2]);
            } else if(string[0] == "SCRIPTSTOPPED"){
                ScriptStopped(evt.data);
            } else if(string[0].substring(0,4)==="PLOT"){
                PlotReceivedData(evt.data);
            } else if(string[0] == "CONNLIST"){ // updated connected devices
                devarray=eval(string[1]);
                    for (var i = 0; i < devarray.length; i++) {
                        log(NOTE, devarray[i]);
                        // reverse search through deviceMap for keys matching device names
                        for (var prop in window.deviceMap){
                            if (window.deviceMap.hasOwnProperty(prop)){
                                if(window.deviceMap[prop]==devarray[i]){
                                    $("."+prop+".ui-accordion-header").removeClass("off").addClass("on");
                                    $("#ConnText" + prop).html('<a href="javascript:WebSocketDelConn(\'' + window.deviceMap[prop] + '\'); void(0);">Disconnect</a>');
                                }
                            }
                        }
                    }
                ws.send("SERVERSTATUS");
            
            } else if(string[0] == "ADDCONN"){
                // reverse search through deviceMap for keys matching device names
                for (var prop in window.deviceMap){
                    if (window.deviceMap.hasOwnProperty(prop)){
                        if(window.deviceMap[prop]==string[1]){
                            $("."+prop+".ui-accordion-header").removeClass("off").addClass("on");
                            $("#ConnText" + prop).html('<a href="javascript:WebSocketDelConn(\'' + window.deviceMap[prop] + '\'); void(0);">Disconnect</a>');
                        }
                    }
                }
            } else if(string[0] == "DELCONN"){
                // reverse search through deviceMap for keys matching device names
                for (var prop in window.deviceMap){
                    if (window.deviceMap.hasOwnProperty(prop)){
                        if(window.deviceMap[prop]==string[1]){
                            $("."+prop+".ui-accordion-header").removeClass("on").addClass("off");
                            $("#ConnText" + prop).html('<a href="javascript:WebSocketAddConn(\'' + window.deviceMap[prop] + '\'); void(0);">Connect</a>'); 
                       }
                    }
                }
            } else if(string[0]=="SERVERSTATUS"){
              $('#WebThreads').html(string[1]);
              $('#DevThreads').html(string[2]);
              $('#PlotThreads').html(string[3]);
              $('#ScriptThreads').html(string[4]);
              $('#LockThreads').html(string[5]);
            }
        
        }
        
     };
     
     ws.onclose = function()
     { 
        // websocket is closed.
        log(ERROR, "Connection is closed"); 
        ws.send('CLOSE');
        ws.close();
        $(".ui-accordion-header").removeClass("on").addClass("off");
        $(".util.ui-accordion-header").removeClass("off");
        for (var prop in window.deviceMap){
            if (window.deviceMap.hasOwnProperty(prop)){
            $("#ConnText" + prop).html('<a href="javascript:WebSocketAddConn(\'' + window.deviceMap[prop] + '\'); void(0);">Connect</a>');
        }}
     };
     
     
  }
  else
  {
     // The browser doesn't support WebSocket
     log(ERROR, "WebSocket is not supported by your browser!");
  }
}

function WebSocketSend(message){ //wrapper for sending websocket messages
    if (! checkWebSocket()){
        alert("Not connected to server!");
        return false;
    }
    log(OUTPUT, message);
    ws.send(message);

    return true;
}


function WebSocketAddConn(device){
    WebSocketSend('ADDCONN;' + device);
}

function WebSocketDelConn(device){
    WebSocketSend('DELCONN;' + device);
}

function WebSocketStop(){
    WebSocketSend('CLOSE');
    ws.close();
    $('#experiment').html('');
    $(".ui-accordion-header").removeClass("on").addClass("off");
    $(".util.ui-accordion-header").removeClass("off");
}

  
 
