// JUST IT WILL MANIPULE THE SCREEN
game.screen = {
  start: function(){
    game.out("game.screen.start");
    
    $('<div/>', {  
      id: '_game',
      'class':'_game',
      css: {
        position: 'relative',
        border: '1px solid #f00',
      },
    }).appendTo($('body'));
    
    /*
    $('<div/>', {  
      id: '_map',
      css: {
        position: 'relative',
        border: '1px solid #0ff',
        margin: '0 auto',
      },
    }).appendTo($('#_game'));
    
     $('<div/>', {  
      id: '_ground',
      css: {
        position: 'absolute',
        //border: '1px solid #ff0',
        top: 0,
        left: 0,
        zIndex: 0,
      },
      dblclick: game.listener.ground.dblclick,
    }).droppable({
      drop: game.listener.ground.drop
      }).appendTo($('#_map'));
    
    
    $('<div/>', {  
      id: '_items',
      css: {
        position: 'absolute',
        border: '1px solid #0f0',
        top: 0,
        left: 0,
        zIndex: 1,
      },
    }).appendTo($('#_map'));
    
    $('<div/>', {  
      id: '_chars',
      css: {
        position: 'absolute',
        border: '1px solid #00f',
        top: 0,
        left: 0,
        zIndex: 2,
      },
    }).appendTo($('#_map'));
    */
  },
  
  server: {
    hour: function(server_hour){
      //game.out("game.screen.server.hour server_hour:"+dump(server_hour));
      _server_hour = $('#_server_hour');
      if (_server_hour.length == 0){
        _server_hour = $('<div/>', {  
          id: '_server_hour',
          'class':'_server_hour',
          css: {
            position: 'absolute',
            top: 0,
            right: 0,
            border: '1px solid #0ff',
          },
        });
        _server_hour.appendTo($('#_game'));
      }
      //alert('hour:'+server_hour);
      _server_hour.html(server_hour);
    },
    delay: function(server_delay){
      //game.out("game.screen.server.hour server_hour:"+dump(server_hour));
      _server_delay = $('#_server_delay');
      if (_server_delay.length == 0){
        _server_delay = $('<div/>', {  
          id: '_server_delay',
          'class':'_server_delay',
          css: {
            position: 'absolute',
            top: 20,
            right: 0,
            border: '1px solid #00f',
          },
        });
        _server_delay.appendTo($('#_game'));
      }
      //alert('delay:'+server_delay);
      _server_delay.html(server_delay);
    },
  },
  
  self: {
    update: function(self){
      // THIS FUNCTION IS NOT IMPLEMENTED
      game.out("game.screen.self (NOTHING) self:"+dump(self));
    },
  },
  
  place: function(place){
    game.out("game.screen.place UPDATING PLACE");
    
    _place = $('#_'+place.id)
    
    // if it is not created
    if (_place.length == 0){
      _place = $('<div/>', {  
        id: '_'+place.id,
        'class':'_place',
        css: {
          position: 'relative',
          border: '1px solid #0ff',
          margin: '0 auto',
        },
      });
      
      // DOUBLE CLICK IS FOR MOVE EVENT,
      // THAN IT CAN ONLY OCCOURS IN PLACE TYPE MAP
      // *** EU ACHO QUE SOH VAI TER UM MAPA EM TELA !!!
      if (place.type == 'place'){
        _place.dblclick(game.listener.place.dblclick);
      }
      _place.appendTo($('#_game'));
      //alert('creatted and appended');
    }
    
    css_properties = {}
    if (typeof(place.w) == 'number'){
      css_properties.width = place.w*32
      game.out("place w: "+place.w);
    }
    if (typeof(place.h) == 'number'){
      css_properties.height = place.h*32
      game.out("place h: "+place.h);
    }
    
    _place.css(css_properties);
    
    
    if (typeof(place.ground) == 'object'){
      _ground = $('#_'+place.id+' ._ground');
      //alert('creating:'+_ground.length);
      if (_ground.length == 0){
        //game.out('game.screen.place CREATING GROUND DIV');
        _ground = $('<div/>', {  
          'class': '_ground',
          css: {
            position: 'absolute',
            //border: '1px solid #ff0',
            top: 0,
            left: 0,
            zIndex: 0,
          },
        });
        /*
        // NOT IMPLEMENTED YET THIS DROP OF THE ITEMS
        _ground.droppable({
          drop: game.listener.ground.drop
        });
        */
        _ground.appendTo(_place);
      }
      //alert('created:'+_ground.length);
      
      game.out('game.screen.place DELETING GROUNDS');
      _ground.children().each(function() {
          $(this).remove();
        });
      
      game.out('game.screen.place INSERTING NEW GROUNDS');
      for (i in place.ground){
        //game.out("game.screen.place ground["+i+"]: "+place.ground[i]);
        var image = document.createElement('img');
        image.src = './'+place.ground[i]+'.png';
        _ground.append(image);
      }
      //game.out("map ground: "+dump(map.ground));
    }
    //game.out("map ground type: "+typeof(map.ground)+": "+map.ground);
  },
  
  object: function(object){
    // REMEMBER THAT THIS FUNCTIONS IS UPDATING EVERY PROPERTIES,
    // IT MUST TO UPDATE JUST THE CHANGED PROPERTIES !!!
    
    // Here try to take the div where this object type must be added
    // ex for chars, $('#_PLACE ._char')
    _object_place = $('#_'+object.place+' ._'+object.type);
    //alert('creating:'+_ground.length);
    // Here creates a div to this object type
    if (_object_place.length == 0){
      _place = $('#_'+object.place);
      // Here checks if really exist a this object place to put its
      // if it not exist, nothing can be happen
      if (_place.length == 0){
        // Do not have this object.place to put its
        alert('Do not have the place to put this object #_'+object.place)
        return;
      }
      else{
        switch (object.type){
          case 'item':
            zIndex = 1;
            break;
          case 'char':
            zIndex = 2;
            break;
        }
        _object_place = $('<div/>', {  
          'class': '_'+object.type,
          css: {
            position: 'absolute',
            top: 0,
            left: 0,
            zIndex: zIndex,
          },
        });
        _object_place.appendTo(_place);
      }
    }
    
    _object = $('#_'+object.id);
    if (_object.length == 0){
      // I NEED TO CHECK object.x AND object.y
      _object = $('<div/>', {  
        id: '_'+object.id,
        css: {
          position: 'absolute',
          left: object.x*32,
          top: object.y*32,
          width: 32,
          height: 32,
          border: '1px solid #ccc',
          overflow: 'hidden'
        },
        onclick: "game.out('Clicked char:'+this.id)",
      });
      _object.appendTo(_object_place);
    }
    
    _object_image = null;
    if (true){ // if (object.image){
      _object_image = _object.children('._image');
      if (_object_image.length == 0){
        _object_image = $('<img/>', {  
          'class': '_image',
          // not implemented yet
          //src: './'+object.image+'.png',
          src: './char.png',
          css: {
            position: 'absolute',
            top: 0,
            left: 0
          }
        });
        _object_image.appendTo(_object);
      }
    }
    
    animate_properties = {}
    // not using
    //css_property = {}
    if (typeof(object.x) == 'number'){
      animate_properties.left = object.x*32
      //game.out("NEWX: "+char.x+" left = "+char.x*32);
    }
    
    if (typeof(object.y) == 'number'){
      animate_properties.top = object.y*32
      //game.out("NEWY: "+char.y+" top = "+char.y*32);
    }
    
    if (typeof(object.direction) == 'number'){
      if (_object_image){ // <--- I THINK THAT IT IS SUX
        _object_image.css('top', -object.direction*32)
        game.out("NEW DIRECTION: "+object.direction);
      }
    }
    // stop will clear animation queue and complete immediately
    _object.stop(true, true);
    _object.animate(animate_properties, 1000);
    // its for tile animate (feet moving)
    if (typeof(object.x) == 'number' || typeof(object.y) == 'number'){
      _object_image.stop(true, true);
      _object_image.delay(250).animate({'left': 0}, 0);
      _object_image.delay(250).animate({'left': -32}, 0);
      _object_image.delay(250).animate({'left': -64}, 0);
      _object_image.delay(250).animate({'left': -32}, 0);
    }
    
  },
  /*  
    update: function(char){
      game.out("game.screen.char.update: "+dump(char));
      animate_properties = {}
      // not using
      //css_property = {}
      if (typeof(char.x) == 'number'){
        animate_properties.left = char.x*32
        //game.out("NEWX: "+char.x+" left = "+char.x*32);
      }
      
      if (typeof(char.y) == 'number'){
        animate_properties.top = char.y*32
        //game.out("NEWY: "+char.y+" top = "+char.y*32);
      }
      
      if (typeof(char.direction) == 'number'){
        $('#_c'+char.id+' img').css('top', -char.direction*32)
        game.out("NEW DIRECTION: "+char.direction);
      }
      // stop will clear animation queue and complete immediately
      $('#_c'+char.id).stop(true, true).animate(animate_properties, 1000);
      // its for tile animate (feet moving)
      $('#_c'+char.id+' img').stop(true, true).delay(250).animate({'left': 0}, 0).delay(250).animate({'left': -32}, 0).delay(250).animate({'left': -64}, 0).delay(250).animate({'left': -32}, 0);
    },
  },
  */
  /*
  items: {
    add: function(item){
      $('<img/>', {  
        id: '_i'+item.id,
        src: './item.png',
        css: {
          position: 'absolute',
          left: item.x*32,
          top: item.y*32,
          width: 32,
          height: 32,
        },
        onclick: "game.out('Clicked item:'+this.id)",
      }).draggable({
          grid: [32, 32],
          zIndex: 4,
          opacity: 0.50,
          revert: true,//make it back to original position
          helper: 'clone',//make a clone to move
        }).appendTo($('#_items'));
    },
    
    update: function(item){
      // if is set char.x
      animate_properties = {}
      // not using
      //css_property = {}
      if (typeof(item.x) == 'number'){
        animate_properties.left = item.x*32
        //game.out("NEWX: "+char.x);
      }
      
      if (typeof(item.y) == 'number'){
        animate_properties.top = item.y*32
        //game.out("NEWY: "+char.y);
      }
      $('#_i'+item.id).animate(animate_properties, 1000);
    },
    
    remove: function(item){
      $('#_i'+item.id).remove();
    },
  }
  */
};
