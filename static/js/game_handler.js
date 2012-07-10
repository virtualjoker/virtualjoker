game.handler = {
  response: function(response){
    //game.out('game.handler.response :'+dump(response));
    if (typeof response.channel_token != 'undefined'){
      game.channel.open(response.channel_token);
    }
    
    if (typeof response.server_hour != 'undefined'){
      //alert('hand: hour:'+response.server_hour);
      game.data.server.hour = response.server_hour;
      game.screen.server.hour(game.data.server.hour);
    }
    
    if (typeof response.server_delay != 'undefined'){
      game.data.server.delay = response.server_delay;
      game.screen.server.delay(game.data.server.delay);
    }
  
    if (typeof response.self != 'undefined'){
      this.self(response.self);
    }
    
    if (typeof response.place != 'undefined'){
      game.out('game.handler.message place:'+dump(response.place));
      this.place(response.place);
    }
    
    
    
    if (typeof response.objects != 'undefined'){
      for (id in response.objects){
        game.out('game.handler.message objects:'+dump(response.objects[id]));
        this.objects(response.objects[id]);
      }
    }
    
    // stop here just for development
    // after it this is not implemented
    return;
    
    // HANDLERS NOT IMPLEMENTED YET
    if (typeof response.message != 'undefined')
      this.message(response.message);
    
    if (typeof response.alert != 'undefined')
      this.alert(response.alert);
    
    if (typeof response.error != 'undefined')
      this.error(response.error);
  },
  
  self: function(self){
    // NOT IMPLEMENTED YET
    //game.out('game.handler.self :'+dump(self));
    game.data.self = self;
    game.screen.self.update(self);
  },
  
  place: function(place){
    if (!game.data.place[place.id]){
      game.data.place[place.id] = place;
    }
    else{
      // Object id and type needed to atualize screen
      // Object id will be sent every time
      // and if type wasn't sent, it must to be added
      if (typeof place.type == 'undefined')
        place.type = game.data.place[place.id].type
      
      for (property in place){
        //game.out("game.handler.map map['"+property+"']:"+map[property]);
        game.data.place[place.id][property] = place[property];
      }
    }
    game.screen.place(place);
  },
  
  objects: function(object){
    if (!game.data.objects[object.id]){
      //game.out("newchar id:"+id+" x: "+chars[id].x);
      //game.out("game.chars.set new char['"+id+"']: "+dump(chars));
      //if (typeof(chars['x'])
      game.data.objects[object.id] = object;
    }
    // else, this char already exist in the screen (and in the list)
    else{
      // Here we will atualize the chars propertys
      
      // Object id, type and place needed to atualize screen
      // Object id will be sent every time
      // and if type or place wasn't sent, it must to be added
      if (typeof object.type == 'undefined')
        object.type = game.data.objects[object.id].type
      if (typeof object.place == 'undefined')
        object.place = game.data.objects[object.id].place
      
      
      direction = null;
      
      for (attr in object){
        game.out("game.handler.object update object['"+object.id+"']['"+attr+"']:"+object[attr]);
        if (object.type == 'char'){
          // DECIDING DIRECTIONS
          // BY TILES CONVENSION: 0=SOUTH, 1=WEST, 2=EAST, 3=NORTH
          switch (attr){
            case 'x':
                if (object[attr] > game.data.objects[object.id][attr])
                  direction = 2;
                else if (object[attr] < game.data.objects[object.id][attr])
                  direction = 1;
              break;
            
            case 'y':
                if (object[attr] > game.data.objects[object.id][attr])
                  direction = 0;
                else if (object[attr] < game.data.objects[object.id][attr])
                  direction = 3;
              break;
          }
        }
        
        game.data.objects[object.id][attr] = object[attr];
      }
      
      if (direction != null){
        object['direction'] = direction;
        game.data.objects[object.id]['direction'] = object['direction'];
      }
      
      
    }
    
    
    game.screen.object(object);
  },
  /*
  item: function(item){
    // Removed item
    if (typeof(item.remove) != 'undefined'){
      //NOT WORKING
      //game.data.items.splice(items[id].id, 1);
      delete game.data.object[item.id]
      game.screen.items.remove(item);
      continue;
    }
    // If is a new char
    if (!game.data.object[item.id]){
      //game.out("newchar id:"+id+" x: "+chars[id].x);
      //game.out("game.chars.set new char['"+id+"']: "+dump(chars));
      //if (typeof(chars['x'])
      game.data.object[item.id] = item;
      game.screen.items.add(item);
    }
    // else, this char already exist in the screen (and in the list)
    else{
      // Here we will atualize the chars propertys
      for (attr in item){
        //game.out("game.chars.set update char['"+id+"']['"+property+"']:"+chars[id][property]);
        game.data.object[item.id][attr] = item[attr];
      }
      game.screen.items.update(item);
      
    }
  },
  */
  messages: function(messages){
    // NOT IMPLEMENTED YET
    //game.out('game.handler.messages :'+dump(messages));
    for (i in messages){
      game.out(messages[i], 'message');
    }
  },
  
  alerts: function(alerts){
    // NOT IMPLEMENTED YET
    //game.out('game.handler.alerts :'+dump(alerts));
    for (i in alerts){
      game.out(alerts[i], 'alert');
    }
  },
  
  errors: function(errors){
    // NOT IMPLEMENTED YET
    //game.out('game.handler.errors :'+dump(errors));
    for (i in errors){
      game.out(errors[i], 'error');
    }
  },
  
  start: function(){
    game.out("game.handler.start");
  }
};
