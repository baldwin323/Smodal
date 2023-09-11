module.exports = -> 
    try

        #
        # users can define HOME/.notice/middleware.js
        #

        require "#{  process.env.HOME  }/.notice/middleware"


    catch error

        #
        # if they want to
        #

        {}
