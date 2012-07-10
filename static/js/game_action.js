game.action = {
  timeout: 10000, // Forcing the error
  sendtime: 0,
  beforesend: function(XMLHttpRequest, settings){
    game.out('beforesend settings:'+settings.data);
  },
  error: function(XMLHttpRequest, error){
    game.out('game.action.error XMLHttpRequest: error:'+error);
    //game.out('XMLHttpRequest:'+dump(XMLHttpRequest));
    
  },
  sucess: function(data, textStatus, XMLHttpRequest){
    game.out('game.action.sucess data:'+data+', textStatus:'+textStatus);
    game.out('game.action.sucess data:'+dump(data));
    game.handler.response(data);
  },
  complete: function(XMLHttpRequest, textStatus){
    // "success", "notmodified", "error", "timeout", or "parsererror"
    //game.out('complete textStatus:'+textStatus);
    completetime = new Date().getTime();
    latency = completetime - game.action.sendtime;
    game.out("game.action.complete latency = "+latency+" status = "+textStatus);
  },
  // Here is an example how to call this function:
  // game.send('funcao_teste', ['up','down', 23452]);
  // never forget that the args is an Array of args
  // ALL EMPTY ARG WILL BE REMOVED ON THE HOST
  send: function(action, args, url) {
    
    // To mensure the latency
    this.sendtime = new Date().getTime();
    
    if (!url) // this is seted because it can be called to /state too
      url = 'action';
    
    // If optional arguments was not provided, create it as empty
    if (!args)
      args = new Array();
    
    // If optional argument was a just one string, it must be an Array
    if (typeof(args) == 'string')
      args = new Array(args);
    
    
    game.out("game.action.send action:" + action + " args:" + dump(args));
    
    $.ajax({
      url: url,
      type: 'POST',
      cache: false,
      dataType: 'json',
      data: ({
        action: action,
        'args[]': args,
        time: game.action.sendtime,
      }),
      timeout: game.action.timeout,
      beforeSend: game.action.beforesend,
      error: game.action.error,
      success: game.action.sucess,
      complete: game.action.complete,
    });
  },
  
  // This action will recive the screen and active the char on game
  start: function(){
    //this.send('send_screen');
    game.out("game.action.start");
  },
  
  // This action will desactive the char on game
  close: function(){
    this.send('close');
  },
  
  // This action must be called when we need to reload all the screen
  // it must to clean the screen before caled this function
  send_screen: function(){
    this.send('send_screen');
  },
  
  move: function(args){
    game.out("game.action.move args:" + dump(args));
    // Sending 2 args with the position where char want to go (x,y)
    /*
    // CHECK IF (x,y) IS INNER THE PLACES SIZE
    // NOT IMPLEMENTED
    w = game.data.map.w;
    h = game.data.map.h;
    if (args[0] >= 0 && args[0] < game.data.map.w &&
        args[1] >= 0 && args[1] < game.data.map.h)
    
    */
      this.send('move', args);
  },
  
  
  move_item: function(args){
    game.out("game.action.move_item args:" + dump(args));
    // Sending 2 args with the position where char want to go (x,y)
    /*
    // CHECK IF (x,y) IS INNER THE PLACES SIZE
    // NOT IMPLEMENTED
    w = game.data.map.w;
    h = game.data.map.h;
    if (args[1] >= 0 && args[1] < game.data.map.w &&
        args[2] >= 0 && args[2] < game.data.map.h)
    */
    this.send('move_item', args);
  },
  
  // This action must be called when we need to reload all the screen
  // it must to clean the screen before caled this function
  get_channel_token: function(){
    game.out("game.action.get_channel_token");
    this.send('get_channel_token');
  },
};
