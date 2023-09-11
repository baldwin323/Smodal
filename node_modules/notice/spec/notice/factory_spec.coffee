require('nez').realize 'Factory', (Factory, test, context, should, os) -> 

    context 'create()', (it) -> 


        it 'requires origin name', (done) -> 

            try 
                Factory.create()

            catch error
                error.should.match /require message originName as string/
                test done


        it 'returns a notifier', (that) -> 

            RECEIVED = []
            notify = Factory.create( 'Message Origin' )


            that 'is used to send messages', (done) -> 

                notify 'test message'
                test done


            that 'has a middleware registrar', (done) -> 

                notify.use (msg, next) -> next() 
                test done


            that 'can further classify the message with type', (done) -> 

                notify.use (msg, next) -> 

                    msg.context.type.should.equal 'info'
                    test done
                    next()

                notify.info 'test message'

            that 'can further classify the message with tenor', (done) -> 

                notify.use (msg, next) -> 

                    msg.context.tenor.should.equal 'bad'
                    test done
                    next()

                notify.info.bad 'test message'
                

            that 'returns the message "promise tail" from middleware pipeline', (done) ->

                notify.info.normal( 'message' ).then.should.be.an.instanceof Function
                test done


            that 'populates the tail resolver with the final message (post middleware)', (done) -> 

                notify.info.normal( 'message' ).then (finalMessage) -> 

                    finalMessage.context.title.should.equal 'message'
                    finalMessage.context.origin.should.equal 'Message Origin'
                    test done

            that 'survives middleware exceptions'
            that 'enables tracable middleware'


            that 'passes the message through the registered middleware', (done) -> 


                notify.use (msg, next) -> 
                    
                    msg.and  = 'THIS'
                    next()

                notify.use (msg, next) -> 

                    msg.also = 'THAT'
                    next()

                 
                notify.info.normal( 'TITLE', 'DESCRIPTION' ).then (msg) ->

                    msg.context.title.should.equal 'TITLE'
                    msg.context.description.should.equal 'DESCRIPTION'

                    msg.and.should.equal 'THIS'
                    msg.also.should.equal 'THAT'
                    test done
