pipeline     = require 'when/pipeline'
Defer        = require('when').defer
Message      = require './message'
Local        = require './local'
isMiddleWare = require('./decorators').isMiddleware
asResolver   = require('./decorators').asResolver


module.exports = Factory =

    #
    # create a message pipeline and 
    # return the notifier (input) 
    # function
    # 

    create: (originName, defaultFn) -> 

        #
        # originName - The origin name for messages sent
        # 
        # defaultFn  - Default middleware receives the assembled
        #              message (After all middleware processing)
        #             

        unless typeof originName is 'string' 

            throw new Error 'Factory.create( originName ) require message originName as string'

        middleware = []
        assigned   = []
        after      = []

        #
        # load personal message middleware from 
        # $HOME/.notice/middleware (if present)
        #

        if Local()[originName]? 

            # 
            # override defaultFn if $HOME/.notice/middleware defined
            # 'originName': function(msg, next) { ... 
            #

            (isMiddleWare asResolver (fn) -> assigned.push fn) Local()[originName]

        else if defaultFn instanceof Function

            (isMiddleWare asResolver (fn) -> assigned.push fn) defaultFn

        else 

            (isMiddleWare asResolver (fn) -> assigned.push fn) (msg, next) -> next()


        if Local().finally? then (

            isMiddleWare asResolver (fn) -> after.push fn

        ) Local().finally


        notifier = (title, descriptionOr, type, tenor) ->

            #
            # notifier() creates a new message object
            #

            message = new Message descriptionOr

            #
            # notifier() creates a deferral to be resolved
            # upon completion of the message's traversal
            # of the middleware pipeline
            #

            Done = Defer()


                                          #
                                          # these args could be hazardous?? 
                                          #
                                          # TODO: understand exactly what v8 does with
                                          #       args being cast into the closure. 
                                          # 
                                          #       if outside calls modify the contents 
                                          #       of the source reference while messages
                                          #       are lagged in the pipeline waiting
                                          #       for middleware that broke out with
                                          #       an async operation, 
                                          #       
                                          #       then the posibility may exist that
                                          #       the original message contents will
                                          #       be modified by any event chains that 
                                          #       are set off in the interim.
                                          # 
                                          #       um? 2> 
                                          # 
                                          #       consider a deep copy
                                          # 
                                          #       also, some kind of introspection on
                                          #       the pipeline lag may be a good idea
                                          # 
                                          # 

            message.title       = title
            message.description = descriptionOr
            message.origin      = originName
            message.type        = type
            message.tenor       = tenor



            #
            # sends it down the middleware pipeline...
            # and returns the promise handler
            #

            functions = []
            
            return pipeline( for fn in middleware.concat(assigned).concat after
                          # 
                          #
                          # the 'value' of fn (function reference) will 
                          # be whichever was last in the array by the 
                          # time the pipeline starts up
                          # 
                          # the pipeline would then call the last 
                          # registered middleware function over and 
                          # over 
                          # 
                          # so each reference is pushed into an array and 
                          # shifted back out in the same sequence as the 
                          # pipeline traverses 
                          #
                          #
                functions.push fn

                                        #
                                        # message, as scoped by the surrounding
                                        # notifier()'s closure, is passed into
                                        # each middleware in turn
                                        # 
                                        # 
                -> functions.shift()(  message  )
                                        # 
            ).then(                     # and then out the exit
                                        # 
                -> Done.resolve      message
                -> Done.reject.apply null, arguments
                -> Done.notify.apply null, arguments

                #
                # included a notify, 
                # 
                # But the notify input has not (yet/ifever) been made
                # abailable to the message middleware.
                #

            )

            return Done.promise


        #
        # returns with API wrap
        #

        api = (title, description) -> notifier title, description, 'info', 'normal'

        api.use   = isMiddleWare asResolver (fn) -> middleware.push fn
        api.info  = (title, description) -> notifier title, description, 'info', 'normal'
        api.event = (title, description) -> notifier title, description, 'event', 'normal'

        api.info.normal  = api.info
        api.info.good    = (title, description) -> notifier title, description, 'info', 'good'
        api.info.bad     = (title, description) -> notifier title, description, 'info', 'bad'

        api.event.normal = api.event 
        api.event.good   = (title, description) -> notifier title, description, 'event', 'good'
        api.event.bad    = (title, description) -> notifier title, description, 'event', 'bad'


        return api

