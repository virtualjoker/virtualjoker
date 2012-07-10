game.feeder = {
  timeout: 30000, // Forcing the error
  sendtime: 0,
  
  error: function(XMLHttpRequest, error){
    game.out('game.feeder.error XMLHttpRequest: error:'+error);
    
  },
  
  complete: function(XMLHttpRequest, textStatus){
    completetime = new Date().getTime();
    life_time = completetime - game.feeder.sendtime;
    game.out("game.feeder.complete life_time = "+life_time+" status = "+textStatus);
    
    // just for development
    //game.feeder.send()
    if (is_develompent)
      timeout = 3000
    else
      timeout = 100
    setTimeout('game.feeder.open()', timeout)
  },
  
  send: function() {
    game.out("game.feeder.send");
    // To mensure the life_time
    this.sendtime = new Date().getTime();
    
    $.ajax({
      url: "feeder",
      type: "POST",
      cache: false,
      timeout: game.feeder.timeout,
      error: game.feeder.error,
      complete: game.feeder.complete,
    });
  },
  
  open: function(){
    this.send();
  },
  
  start: function(){
    game.out("game.feeder.start");
  }
};
