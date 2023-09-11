require('nez').realize 'Local', (Local, test, it, should, Notice) -> 

    it 'loads local messenger module for "Test Source 1" from $HOME/.notice/middleware.js', (done) -> 

        home = process.env.HOME
        process.env.HOME = '../../'
        notice = Notice.create( 'origin' )
        notice.use Local().default
        process.env.HOME = home


        sent = notice.info.normal 'title', 'description'

        sent.then (msg) -> 

            msg.should.eql anything: 'you want'
            test done
