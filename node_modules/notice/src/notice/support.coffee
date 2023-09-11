module.exports = support =

    argsOf: (fn) ->

        #
        # return array of fn's arg names
        # or empty array
        #

        try

            fn.toString().match(

                /function\W*\((.*)\)/ 

            )[1].split(',').map( 

                (arg) -> arg.trim()

            ).filter (arg) -> arg != ''

        catch error

            []

    callsFn: (fn, Fn) -> 

        #
        # true if fn() is called in Fn
        #

        Fn.toString().match( 

            new RegExp "#{fn}\W*\\(\W*\\)" 

        ) instanceof Array
