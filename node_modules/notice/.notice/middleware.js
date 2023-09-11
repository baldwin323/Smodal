// 
// Example personal message middleware
//
// - Always loaded last on the middleware pipeline
// 
// $HOME/.notice/middleware.js
//

module.exports = { 

    "origin name": function( msg, next ) {

        // 
        // override per 'origin name'
        //

        next();

    },

    finally: function( msg, next ) {

        //
        // is always run
        //
        // console.log( JSON.stringify( msg.content, null, 2 ) );
        // console.log( msg.context );
        // console.log( msg );
        //
        // 
        // do anything: 
        // ============
        // 
        // require 'hubot', 'hipchat', 'growl', 'socket.io', 'graphite', 'umm?'
        //
        // but
        // ===
        //
        // call next(), And if you choose to breakout in order to augment the
        //              message with payload from a remote source, be sure to 
        //              only call next() after your query callback data has
        //              been appended to the msg.
        //              
        //              
        // 

        msg.anything = 'you want'
        next();

    }

}
