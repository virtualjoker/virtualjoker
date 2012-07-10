game.channel = {
  lasttime: 0,
  token: null, // setted in index.html
  channel: null,
  socket: null,
  onopen: function(){
    game.out('game.channel.onopen');
    // just for development
    //game.feeder.open()
    if (is_develompent)
      timeout = 3000
    else
      timeout = 100
    setTimeout('game.feeder.open()', timeout)
  },
  onmessage: function(msg){
    timenow = new Date().getTime();
    latency = timenow - game.channel.lasttime;
    game.out('game.channel.onmessage latency:'+latency+' msg.data:'+msg.data);
    game.channel.lasttime = new Date().getTime();
    response = null;
    try{
      response = $.parseJSON(msg.data);
    }catch(e){
      game.out('CHANNEL ERROR parseJSON:"'+e+'"');
    }
    if (response){
      game.handler.response(response);
    }
  },
  onerror: function(msg){
    game.out('game.channel.onerror data:'+dump(msg));
  },
  onclose: function(){
    game.out('game.channel.oncloses');
    this.start();
  },
  open: function(token){
    game.out('game.channel.open');
    
    //this.close()
    
    if (token){
      this.token = token;
      this.channel = new goog.appengine.Channel(this.token);
    }
    
    this.socket = this.channel.open({
      'onopen': game.channel.onopen,
      'onmessage': game.channel.onmessage,
      'onerror': game.channel.onerror,
      'onclose': game.channel.onclose
    });
    this.socket.onopen = this.onopen;
    this.socket.onmessage = this.onmessage;
    this.socket.onerror = this.onerror;
    this.socket.onclose = this.onclose;
  },
  close: function(){
    game.out('game.channel.close');
    //if (this.socket)
    //  this.socket.close();
  },
  start: function(){
    game.out("game.channel.start");
    game.action.get_channel_token();
  }
};
