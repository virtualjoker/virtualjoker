game.listener = {
  start: function(){
    game.out("game.listener.start");
    $(document).keypress(this.keypress);
    //$(document).click(this.click);
  },
  keypress: function(event){
    game.out('keypress: '+event.which);
    switch (event.which){
      case 99: // C CREATE ITEM
        game.action.send('create_item');
        break;
      case 100: // D DELETE ITEM
        game.action.send('delete_item');
        break;
    }
  },
  place: {
    drop: function(event, ui){
      id = ui.draggable.attr('id');
      id = id.replace('_i', '');
      game.out('dropped event:'+event.pageX+','+event.pageY+
               ' ui:'+ui.position.left+','+ui.position.top+' drag.id:'+id)
       game.action.move_item([id, ui.position.left/32, ui.position.top/32])
    },
    dblclick: function(event){
      _object = $(event.target);
      type = get_type(_object);
      while (type != 'ground' && type != 'char' && type != 'item'){
        _object = _object.parent();
        type = get_type(_object);
        if (type == 'game'){
          alert('LOOP DO place.dblclick DEU ERRADO !!!');
          return;
        }
      }
      
      game.out('game.place.dblclick type='+type);
      
      if (type == 'ground'){
        //height = $(window).height();
        //width = $(window).width();
        click_x = event.pageX;
        click_y = event.pageY;
        ground_position = _ground.offset();
        
        // dunno why i put -16px, but it works very well
        x = Math.round((click_x-ground_position.left-16)/32);
        y = Math.round((click_y-ground_position.top-16)/32);
        game.out('map_dbclick click: ('+click_x+', '+click_y+') ground:('+ground_position.left+', '+ground_position.top+') map: x,y: ('+x+', '+y+')');
        game.action.move([x, y]);
      }
    },
  }
};
