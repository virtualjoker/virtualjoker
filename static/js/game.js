get_id = function(object){
  id = object.attr('id');
  if (id)
    return id.substring(1, id.length);
  else
    return null;
}

get_type = function(object){
  type = object.attr('class');
  if (type)
    return type.substring(1, type.length);
  else
    return null;
}


var game = {
  data: {
    server: {
      hour: '',
      delay: '',
    },
    objects: {},
    place: {},
    /*self: {},
    map: {},
    chars: {},
    items: {},*/
  },
  start: function(event) {
    this.out('game.start');
    
    this.action.start();
    this.channel.start();
    this.feeder.start();
    this.handler.start();
    this.listener.start();
    this.screen.start();
    
    
  },
  unload: function(event) {
    this.out('game.unload');
  },
  error: function(event) {
    this.out('game.error: JAVSCRIPT EROR type:"'+event.type+'" data:"'+event.data+'"');
    return true;
  },
  out: function(text, type, time){
    //alert('teste'+$('#_out_active').attr('checked'));
    if (!$('#_out_active').attr('checked')){
      return;
    }
    if (!type)
      type = 'normal'
    if (!time)
      time = 'slow'
    switch (type){
      case 'normal':
        color = '#000000';
        background_color = '#cccccc';
        break;
      case 'message':
        text = 'Message: ' + text;
        color = '#00008b';
        background_color = '#cccccc';
        break;
      case 'alert':
        text = 'Alert: ' + text;
        color = '#ffff00';
        background_color = '#cccccc';
        break;
      case 'error':
        text = 'Error: ' + text;
        color = '#8b0000';
        background_color = '#cccccc';
        break;
      default:
        game.out('You cant send a message with type '+type, 'error')
        return;
    }
    $("<p/>", {
      text: text,
      css: {
        color: color,
        backgroundColor: background_color,
      },
      mouseenter: function(){
        $(this).fadeOut('slow', function() {
          $(this).remove();
        });
      }
    }).appendTo("#_out");
  },
};



$(document).ready(function(event){
  game.start(event);
});

$(window).error(function(event){
  game.error(event);
});

$(window).unload(function(event) {
  game.unload(event);
})
