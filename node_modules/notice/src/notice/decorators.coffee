Defer          = require('when').defer
support        = require './support'
module.exports = 

    #
    #  - ensures fn() is only run once
    #    and only when passed a string
    #

    onceIfString: (fn) -> 
        do (done = false) -> 
            (value) -> unless done 
                if done = typeof value is 'string'
                    fn value


    #
    # - ensures the provided fn is a Function
    # - the decorated function returns false if not
    # 

    isFn: (fn) -> 
        do -> (value) ->
            return fn value if typeof value is 'function'
            return false

    #
    # - ensures the provided fn is valid message middleware
    # - the decorated function returns false if not
    # 

    isMiddleware: (fn) -> 
        (middleware) -> 
            unless next = support.argsOf( middleware )[1]
                console.log 'TODO: silent ignore invalid middleware not good, make plan'
                return -> false
            unless support.callsFn next, middleware
                console.log 'TODO: silent ignore invalid middleware not good, make plan'
                return -> false
            fn middleware

    #
    # - wraps the provided function into a deferral and
    #   calls with the resolver as the middleware `nextFn`
    # - returns the promise
    #

    asResolver: (fn) -> 
        (middleware) -> 
            fn (msg) -> 
                defer = Defer()
                next  = defer.resolve
                middleware msg, next
                defer.promise
                

